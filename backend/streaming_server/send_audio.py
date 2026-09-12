import asyncio
import io
import os
import time

import grpc
import numpy as np
import requests
import websockets
from dotenv import load_dotenv
from pydub import AudioSegment

import audio2face_pb2
import audio2face_pb2_grpc

load_dotenv()

INSTANCE_NAME = "/World/audio2face/PlayerStreaming"
AUDIO2FACE_URL = "localhost:50051"
SAMPLE_RATE = 44100


def require_env(name):
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"{name} is not configured")
    return value


def push_audio_track_stream(url, audio_data, sample_rate, instance_name):
    chunk_size = sample_rate // 10
    sleep_between_chunks = 0.04

    with grpc.insecure_channel(url) as channel:
        stub = audio2face_pb2_grpc.Audio2FaceStub(channel)

        def make_generator():
            yield audio2face_pb2.PushAudioStreamRequest(
                start_marker=audio2face_pb2.PushAudioRequestStart(
                    samplerate=sample_rate,
                    instance_name=instance_name,
                    block_until_playback_is_finished=True,
                )
            )

            for offset in range(0, len(audio_data), chunk_size):
                time.sleep(sleep_between_chunks)
                chunk = audio_data[offset : offset + chunk_size]
                yield audio2face_pb2.PushAudioStreamRequest(
                    audio_data=chunk.astype(np.float32).tobytes()
                )

        response = stub.PushAudioStream(make_generator())
        if not response.success:
            raise RuntimeError(f"Audio2Face rejected audio stream: {response.message}")


def synthesize_and_stream(text):
    elevenlabs_api_key = require_env("ELEVENLABS_API_KEY")
    voice_id = require_env("VOICE_ID")

    response = requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream",
        json={
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "optimize_streaming_latency": "1",
            "voice_settings": {
                "stability": 0.2,
                "similarity_boost": 0.7,
            },
        },
        headers={
            "accept": "*/*",
            "Content-Type": "application/json",
            "xi-api-key": elevenlabs_api_key,
        },
        timeout=60,
    )
    response.raise_for_status()

    audio = AudioSegment.from_file(io.BytesIO(response.content), format="mp3")
    audio = audio.set_channels(1).set_frame_rate(SAMPLE_RATE)
    audio_data = np.frombuffer(audio.raw_data, dtype=np.int16).astype(np.float32) / 32768.0

    push_audio_track_stream(
        AUDIO2FACE_URL,
        audio_data,
        SAMPLE_RATE,
        INSTANCE_NAME,
    )


async def tts_handler(websocket):
    async for message in websocket:
        text = message.strip()
        if not text:
            continue

        print(f"Received text for TTS: {text[:80]}")
        try:
            await asyncio.to_thread(synthesize_and_stream, text)
        except Exception as error:
            print(f"TTS/Audio2Face streaming failed: {error}")


async def serve_forever():
    print("FaceChat TTS WebSocket listening on ws://127.0.0.1:8100")
    async with websockets.serve(tts_handler, "127.0.0.1", 8100):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(serve_forever())
