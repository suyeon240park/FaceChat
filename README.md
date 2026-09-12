# FaceChat: Real-Time Emotion-Driven Text-to-Face Animation

FaceChat is an interactive conversational AI prototype that combines text and voice input, OpenAI Assistants, ElevenLabs text-to-speech, and NVIDIA Audio2Face to generate synchronized facial animation in real time.

The user sends a text or voice message through the web interface. Voice input is transcribed with OpenAI Speech-to-Text, and the resulting text is sent to a configured OpenAI Assistant. The generated response is forwarded to a local WebSocket server, synthesized into speech with ElevenLabs, and streamed to NVIDIA Audio2Face over gRPC. Audio2Face then drives the facial animation rendered through the local WebRTC interface.

FaceChat was built as an HCI prototype exploring more natural and accessible ways to interact with conversational AI. It is not a clinical or healthcare product.

## Demo

[Watch the video demo](https://www.youtube.com/watch?v=jsKBskNUAYM)

[![FaceChat demo](https://github.com/user-attachments/assets/39155820-a99e-44c1-89a7-0098ed3260a1)](https://www.youtube.com/watch?v=jsKBskNUAYM)

## Features

1. **Text Input**: Type messages directly into the chat interface.
2. **Voice Input**: Record voice input using the microphone button or Space bar.
3. **Speech-to-Text**: Transcribe recorded audio using OpenAI Speech-to-Text.
4. **Conversational Response**: Send user input to a configured OpenAI Assistant.
5. **Chat Log**: Display and toggle conversation history in the interface.
6. **Natural Speech**: Convert assistant responses to speech using the ElevenLabs TTS API.
7. **Audio2Face Streaming**: Stream generated audio to NVIDIA Audio2Face over gRPC.
8. **WebRTC Rendering**: Display the animated face through NVIDIA's WebRTC streaming interface.

> Note: `backend/emotion_analysis.py` and `backend/emotion_colab.ipynb` contain experimental emotion-model work. The active runtime path shown in `frontend/js/script.js` and `backend/streaming_server/send_audio.py` does not currently use that model to control the response pipeline.

## Architecture

```text
Text input ───────────────┐
                          ├─> OpenAI Assistant ─> WebSocket ─> ElevenLabs TTS
Microphone -> Speech-to-Text┘                                  |
                                                               v
                                                        NVIDIA Audio2Face
                                                               |
                                                               v
                                                        WebRTC animation
```

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/suyeon240park/FaceChat.git
cd FaceChat
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure credentials

The prototype expects credentials such as:

```text
API_KEY
ASSISTANT_ID
ELEVENLABS_API_KEY
VOICE_ID
```

Do not commit API keys to the repository.

The current frontend was originally developed around NVIDIA Audio2Face's local web bundle and therefore assumes a local development environment rather than a production deployment.

### 5. Install NVIDIA Audio2Face

Install a compatible NVIDIA Omniverse/Audio2Face environment and configure a streaming model.

The project was originally developed against Audio2Face 2023.2.0. The included `backend/streaming_server` and `frontend` files were intended to replace the corresponding local Audio2Face streaming server and WebRTC web files.

### 6. Start the audio streaming server

```bash
python main.py
```

### 7. Serve the frontend

From the frontend directory or the Audio2Face web directory being used:

```bash
python -m http.server
```

Open the local page in a browser and ensure Audio2Face is running.

## Limitations

- The repository is a local prototype rather than a production web service.
- OpenAI requests are issued from frontend JavaScript in the original implementation. A production architecture should proxy these requests through a backend so API credentials are never exposed to the browser.
- The Audio2Face integration depends on a specific local NVIDIA application setup.
- The experimental emotion-analysis code is not currently wired into the active inference path.

## Future Improvements

- move all third-party API calls behind a backend service;
- integrate emotion analysis into the active response/animation pipeline;
- replace local application dependencies with deployable services;
- improve character rendering, lighting, and head/body gestures;
- add automated tests and configuration validation.

## License

This project is licensed under the MIT License. See `LICENSE` for details.
