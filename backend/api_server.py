import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify, request, send_from_directory
from openai import OpenAI

ROOT_DIR = Path(__file__).resolve().parents[1]
FRONTEND_DIR = ROOT_DIR / "frontend"

load_dotenv(ROOT_DIR / ".env")

app = Flask(
    __name__,
    static_folder=str(FRONTEND_DIR),
    static_url_path="",
)


def get_openai_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not configured")
    return OpenAI(api_key=api_key)


def get_assistant_id() -> str:
    assistant_id = os.getenv("OPENAI_ASSISTANT_ID")
    if not assistant_id:
        raise RuntimeError("OPENAI_ASSISTANT_ID is not configured")
    return assistant_id


@app.get("/")
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.get("/api/health")
def health():
    return jsonify(
        {
            "ok": True,
            "openaiConfigured": bool(os.getenv("OPENAI_API_KEY")),
            "assistantConfigured": bool(os.getenv("OPENAI_ASSISTANT_ID")),
        }
    )


@app.post("/api/transcribe")
def transcribe():
    upload = request.files.get("file")
    if upload is None or not upload.filename:
        return jsonify({"error": "Audio file is required."}), 400

    try:
        client = get_openai_client()
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=(
                upload.filename,
                upload.read(),
                upload.mimetype or "application/octet-stream",
            ),
        )
        return jsonify({"text": transcript.text})
    except RuntimeError as error:
        return jsonify({"error": str(error)}), 503
    except Exception as error:
        app.logger.exception("Transcription failed")
        return jsonify({"error": "Transcription failed."}), 502


@app.post("/api/chat")
def chat():
    payload = request.get_json(silent=True) or {}
    message = str(payload.get("message", "")).strip()
    thread_id = payload.get("thread_id")

    if not message:
        return jsonify({"error": "Message is required."}), 400

    try:
        client = get_openai_client()
        assistant_id = get_assistant_id()

        if thread_id:
            # Verify that the supplied thread exists before adding to it.
            client.beta.threads.retrieve(thread_id)
        else:
            thread_id = client.beta.threads.create().id

        client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=message,
        )

        run = client.beta.threads.runs.create_and_poll(
            thread_id=thread_id,
            assistant_id=assistant_id,
        )
        if run.status != "completed":
            return jsonify({"error": f"Assistant run ended with status: {run.status}"}), 502

        messages = client.beta.threads.messages.list(
            thread_id=thread_id,
            order="desc",
            limit=10,
        )

        response_text = None
        for assistant_message in messages.data:
            if assistant_message.role != "assistant":
                continue
            for part in assistant_message.content:
                if part.type == "text":
                    response_text = part.text.value
                    break
            if response_text:
                break

        if not response_text:
            return jsonify({"error": "Assistant returned no text response."}), 502

        return jsonify({"thread_id": thread_id, "response": response_text})
    except RuntimeError as error:
        return jsonify({"error": str(error)}), 503
    except Exception:
        app.logger.exception("Assistant request failed")
        return jsonify({"error": "Assistant request failed."}), 502


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
