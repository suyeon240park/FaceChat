# Generate streaming audio from ElevenLabs TTS service and send it to Audio2Face streaming player in a real time
# Directory: C:\Users\{User}\AppData\Local\ov\pkg\audio2face-2023.2.0\exts\omni.audio2face.player\omni\audio2face\player\scripts\streaming_server
# 1. Open a websockets server
# 2. openai_api(): receive the openai response from script.js
# 3. main(): generate mp3 audio file from ElevenLabs TTS API and convert its type to float32 array
# 4. push_audio_track_stream(): splits audio data into chunks and send them to audio2face streaming player via gRPC requests

import os
import time
import audio2face_pb2
import audio2face_pb2_grpc
import grpc
import numpy as np
import requests
from pydub import AudioSegment
import io
import websockets
import asyncio

# Define ElevenLabs TTS API key and its voice ID
elv_api_key = os.getenv('ELEVENLABS_API_KEY')
voice_id = os.getenv('VOICE_ID')

# Global variables (const)
instance_name = "/World/audio2face/PlayerStreaming"
samplerate = 44100


# Send audio data to audio2face streaming player via gRPC requests
def push_audio_track_stream(url, audio_data, samplerate, instance_name):
    chunk_size = samplerate // 10
    sleep_between_chunks = 0.04
    block_until_playback_is_finished = True

    # Connect to audio2face through grpc
    with grpc.insecure_channel(url) as channel:
        print("Channel creadted")
        stub = audio2face_pb2_grpc.Audio2FaceStub(channel)

        def make_generator():
            # Send a message with start_marker and declare the start of sending data
            start_marker = audio2face_pb2.PushAudioRequestStart(
                samplerate=samplerate,
                instance_name=instance_name,
                block_until_playback_is_finished=block_until_playback_is_finished,
            )
            yield audio2face_pb2.PushAudioStreamRequest(start_marker=start_marker)
            
            # Send messages with audio_data chunks
            for i in range(len(audio_data) // chunk_size + 1):
                time.sleep(sleep_between_chunks)
                chunk = audio_data[i * chunk_size : i * chunk_size + chunk_size]
                yield audio2face_pb2.PushAudioStreamRequest(audio_data=chunk.astype(np.float32).tobytes())

        request_generator = make_generator()
        print("Sending audio data...")
        response = stub.PushAudioStream(request_generator)

        if response.success:
            print("SUCCESS")
        else:
            print(f"ERROR: {response.message}")

    print("Channel closed")

# Generate mp3 audio file from ElevenLabs TTS API and convert its type to float32 array
def main(text):
    # URL of the Audio2Face Streaming Audio Player server (where A2F App is running)
    url = "localhost:50051"

    # Send API request to ElevenLabs TTS
    elv_url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream"

    headers = {
        "accept": "*/*",
        "Content-Type": "application/json",
        "xi-api-key": elv_api_key
    }

    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "optimize_streaming_latency": "1",
        "voice_settings": {
            "stability": 0.2,
            "similarity_boost": 0.7
        }
    }

    # Make the POST request to the ElevenLabs API
    response = requests.post(
        elv_url,
        json=data,
        headers=headers,
    )
    response.raise_for_status()

    mp3_data = bytearray()

    # Read MP3 data from response
    for chunk in response.iter_content(chunk_size=1024):
        if chunk:
            mp3_data.extend(chunk)

    # Convert mp3 to float32 array
    mp3_stream = io.BytesIO(mp3_data) # Create an in-memory byte stream
    audio = AudioSegment.from_file(mp3_stream, format="mp3") # Load MP3 data from the byte stream
    raw_data = audio.raw_data # Convert to raw data
    audio_data = np.frombuffer(raw_data, dtype=np.int16) # Convert to numpy array
    data = audio_data.astype(np.float32) / 32768.0 # Normalize to float32

    # Push the audio track to audio2face streaming audio player
    push_audio_track_stream(url, data, samplerate, instance_name)


# Connects to the WebSocket server and receives the OpenAI Assistant response
async def openai_api(websocket, path):
    async for message in websocket:
        print(f"Received: {message}")
        await main(message)

# Start the websockets server
start_server = websockets.serve(openai_api, "localhost", 8100)

# Run the server forever
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()