# FaceChat: Real-Time Conversational AI Avatar

FaceChat is an interactive conversational AI prototype that combines text and voice input, OpenAI Assistants, ElevenLabs text-to-speech, and NVIDIA Audio2Face to generate synchronized facial animation in real time.

The user sends a text or voice message through the web interface. Voice input is sent to a local Flask backend for OpenAI Speech-to-Text, and text messages are sent through the same backend to a configured OpenAI Assistant. The generated response is then forwarded over a local WebSocket to the ElevenLabs/Audio2Face audio pipeline. Audio2Face drives the facial animation rendered through NVIDIA's WebRTC interface.

FaceChat was built as an HCI prototype exploring more natural and accessible ways to interact with conversational AI. It is not a clinical or healthcare product.

## Demo

[Watch the video demo](https://www.youtube.com/watch?v=jsKBskNUAYM)

[![FaceChat demo](https://github.com/user-attachments/assets/39155820-a99e-44c1-89a7-0098ed3260a1)](https://www.youtube.com/watch?v=jsKBskNUAYM)

## Features

1. **Text Input**: Type messages directly into the chat interface.
2. **Voice Input**: Record voice input using the microphone button or Space bar.
3. **Speech-to-Text**: Transcribe recorded audio through a local backend proxy using OpenAI Speech-to-Text.
4. **Conversational Response**: Send user input through the backend to a configured OpenAI Assistant.
5. **Chat Log**: Display and toggle conversation history in the interface.
6. **Natural Speech**: Convert assistant responses to speech using ElevenLabs TTS.
7. **Audio2Face Streaming**: Stream generated audio to NVIDIA Audio2Face over gRPC.
8. **WebRTC Rendering**: Display the animated face through NVIDIA's WebRTC streaming interface.

> Note: `backend/emotion_analysis.py` and `backend/emotion_colab.ipynb` contain experimental emotion-model work. The active runtime path does not currently use that model to control the response pipeline.

## Architecture

```text
Text input ------------------------------┐
                                         v
Microphone -> Flask backend -> OpenAI Speech-to-Text
                         |               |
                         |               v
                         +--------> OpenAI Assistant
                                         |
                                         v
Browser <--------------------------- text response
  |
  v
WebSocket :8100 -> ElevenLabs TTS -> Audio2Face gRPC :50051
                                      |
                                      v
                               WebRTC animation
```

All OpenAI credentials remain in the local Python backend. The browser no longer reads API keys from `process.env` or sends requests directly to OpenAI.

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

`pydub` also requires FFmpeg to be installed and available on your system PATH.

### 4. Configure credentials

Copy the environment template:

```bash
cp .env.example .env
```

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Then fill in:

```env
OPENAI_API_KEY=<your_openai_api_key>
OPENAI_ASSISTANT_ID=<your_assistant_id>
ELEVENLABS_API_KEY=<your_elevenlabs_api_key>
VOICE_ID=<your_elevenlabs_voice_id>
```

Do not commit `.env`.

### 5. Install and configure NVIDIA Audio2Face

FaceChat was originally developed against NVIDIA Audio2Face 2023.2.0. Start an Audio2Face scene with the Streaming Audio Player available on local gRPC port `50051`, and start NVIDIA's WebRTC streaming service for the avatar view.

The included generated gRPC files under `backend/streaming_server` implement the local Audio2Face audio protocol used by the prototype.

### 6. Start FaceChat

```bash
python main.py
```

This starts:

- the Flask API/static server on `http://127.0.0.1:5000`;
- the local text-to-speech WebSocket on `ws://127.0.0.1:8100`.

Open `http://127.0.0.1:5000` in a browser. NVIDIA's WebRTC player may also require its streaming server IP through the existing `?server=<ip-address>` query parameter, depending on the Audio2Face setup.

## Backend API

The local Flask server exposes three small endpoints:

- `GET /api/health` — reports whether required OpenAI configuration is present;
- `POST /api/transcribe` — accepts a recorded audio file and returns text;
- `POST /api/chat` — accepts a message and optional Assistant thread ID and returns the assistant response.

The frontend only talks to these same-origin local endpoints, so OpenAI credentials are not exposed to browser JavaScript.

## Limitations

- The repository is a local prototype rather than a deployable production service.
- The Audio2Face integration depends on NVIDIA's local application and WebRTC setup.
- The experimental emotion-analysis code is not wired into the active inference path.
- The project uses the OpenAI Assistants workflow and dependency versions from the period in which the prototype was developed; a modern production rewrite should use the current supported OpenAI API surface.
- There are no automated integration tests for the external OpenAI, ElevenLabs, Audio2Face, or WebRTC services.

## Future Improvements

- replace the local NVIDIA application dependency with a deployable animation service;
- integrate emotion analysis only after evaluating whether it improves the interaction experience;
- add backend authentication, request validation, rate limiting, and structured logging;
- add automated unit tests plus mocked integration tests for external services;
- improve character rendering, lighting, and head/body gestures.

## License

This project is licensed under the MIT License. See `LICENSE` for details.
