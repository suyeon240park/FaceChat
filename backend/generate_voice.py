import os
import sys
import audio2face_pb2
import audio2face_pb2_grpc
import requests
import numpy as np
import asyncio

# Set environment variables
elevenlabs_api_key = os.getenv('ELEVENLABS_API_KEY')
voice_id = os.getenv('VOICE_ID')

# Define the URL and headers for the API request
elv_url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream"

headers = {
    "accept": "*/*",
    "Content-Type": "application/json",
    "xi-api-key": elevenlabs_api_key
}

data = {
    "text": (
        "Sweet?"
    ),
    "model_id": "eleven_monolingual_v1",
    "optimize_streaming_latency": "2",
    "output_format": "mp3_44100_128",
    "voice_settings": {
        "stability": 0.1,
        "similarity_boost": 0.7
    }
}

def main():
    # URL of the Audio2Face Streaming Audio Player server (where A2F App is running)
    a2f_url = "localhost:50051"  # ADJUST

    # Prim path of the Audio2Face Streaming Audio Player on the stage (were to push the audio data)
    instance_name = "/World/audio2face/player_streaming_instance"

    # Make the POST request to the ElevenLabs API
    response = requests.post(
        a2f_url,
        json=data,
        headers=headers,
        stream=True
    )
    response.raise_for_status()

    # Sample rate is 44.1kHz
    samplerate = 44100

    # Only Mono audio is supported
    if len(audio_data.shape) > 1:
        audio_data = np.average(audio_data, axis=1)

    with grpc.insecure_channel(elv_url) as channel:
        print("Channel created")
        stub = audio2face_pb2_grpc.Audio2FaceStub(channel)

        def make_generator():
            start_marker = audio2face_pb2.PushAudioRequestStart(
                samplerate=samplerate,
                instance_name=instance_name,
                block_until_playback_is_finished=True,
            )
            yield audio2face_pb2.PushAudioStreamRequest(start_marker=start_marker)

            # Assuming audio_data is received as a stream of chunks
            for chunk in response.iter_content(chunk_size=4096):
                # Convert the chunk to a NumPy array
                array = np.frombuffer(chunk.raw_data, dtype=np.int16)

                # Normalize the array to [-1, 1]
                array = array / 2**15

                # Convert the array back to bytes
                output = array.astype(np.float32).tobytes()
                # audio_data=chunk.astype(np.float32).tobytes()

                yield audio2face_pb2.PushAudioStreamRequest(output)

        request_generator = make_generator()
        print("Sending audio data...")

        response = stub.PushAudioStream(request_generator)
        if response.success:
            print("SUCCESS")
        else:
            print(f"ERROR: {response.message}")

    print("Channel closed")


if __name__ == "__main__":
    asyncio.run(main())

    
"""
    # Read and process streaming data
    for chunk in response.iter_content(chunk_size=4096):
        # Convert the chunk to a NumPy array
        array = np.frombuffer(chunk.raw_data, dtype=np.int16)

        # Normalize the array to [-1, 1]
        array = array / 2**15

        # Convert the array back to bytes
        output = array.astype(np.float32).tobytes()
        # Convert the accumulated audio bytes from MP3 to PCM
        #audio_segment = AudioSegment.from_file(io.BytesIO(audio_bytes), format="mp3")
        #pcm_data = np.array(audio_segment.get_array_of_samples()).astype(np.float32)
        #pcm_data /= np.iinfo(np.int16).max

        # Each audio sample is encoded as 4 bytes (float32)
        #audio_data = base64.b64encode(pcm_data.tobytes())
"""
