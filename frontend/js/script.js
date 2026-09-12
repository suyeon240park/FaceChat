const socket = new WebSocket("ws://localhost:8100");

socket.onopen = () => console.log("Audio WebSocket connection opened");
socket.onclose = () => console.log("Audio WebSocket connection closed");
socket.onerror = (error) => console.error("Audio WebSocket error:", error);

const chatInput = document.querySelector(".text-input");
const sendButton = document.querySelector("#send-btn");
const logsContainer = document.querySelector("#logs");
const buttonIcon = document.querySelector("#log-btn i");
const speakButton = document.getElementById("speak-btn");

function appendLog(label, text) {
  const row = document.createElement("div");
  row.classList.add("logs");

  const paragraph = document.createElement("p");
  const strong = document.createElement("strong");
  strong.textContent = `${label}: `;
  paragraph.appendChild(strong);
  paragraph.appendChild(document.createTextNode(text));

  row.appendChild(paragraph);
  logsContainer.appendChild(row);
}

document.addEventListener("DOMContentLoaded", () => {
  let threadId = null;
  let isRecording = false;
  let mediaRecorder = null;
  let audioChunks = [];

  async function transcribeAudio(audioBlob) {
    const formData = new FormData();
    const extension = audioBlob.type.includes("webm") ? "webm" : "audio";
    formData.append("file", audioBlob, `recording.${extension}`);

    const response = await fetch("/api/transcribe", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || "Transcription failed.");
    }

    return data.text || "";
  }

  async function getChatResponse(userText) {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        message: userText,
        thread_id: threadId,
      }),
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || "Assistant request failed.");
    }

    threadId = data.thread_id;
    return data.response;
  }

  async function startRecording() {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorder = new MediaRecorder(stream);
      audioChunks = [];

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunks.push(event.data);
        }
      };

      mediaRecorder.onstop = async () => {
        const mimeType = mediaRecorder?.mimeType || "audio/webm";
        const audioBlob = new Blob(audioChunks, { type: mimeType });
        audioChunks = [];

        try {
          const text = await transcribeAudio(audioBlob);
          chatInput.value = text;
        } catch (error) {
          console.error(error);
          appendLog("System", error.message || "Transcription failed.");
        } finally {
          stream.getTracks().forEach((track) => track.stop());
        }
      };

      mediaRecorder.start();
      isRecording = true;
      speakButton.innerHTML = '<div class="speaker_on"></div>';
    } catch (error) {
      console.error("Error accessing microphone:", error);
      appendLog("System", "Microphone access failed.");
    }
  }

  function stopRecording() {
    if (!mediaRecorder || mediaRecorder.state === "inactive") return;
    mediaRecorder.stop();
    isRecording = false;
    speakButton.innerHTML = '<i class="fas fa-microphone"></i>';
  }

  async function handleOutgoingChat() {
    const userText = chatInput.value.trim();
    if (!userText) return;

    chatInput.value = "";
    sendButton.innerHTML = '<div class="loader"></div>';
    sendButton.disabled = true;
    appendLog("User", userText);

    try {
      const response = await getChatResponse(userText);
      appendLog("Assistant", response);

      const ttsText = response.replace(/,/g, " --").replace(/\./g, "...");
      if (socket.readyState === WebSocket.OPEN) {
        socket.send(ttsText);
      } else {
        appendLog("System", "Audio2Face WebSocket is not connected; text response is still available.");
      }
    } catch (error) {
      console.error(error);
      appendLog("System", error.message || "Request failed.");
    } finally {
      sendButton.innerHTML = '<i class="fas fa-paper-plane"></i>';
      sendButton.disabled = false;
    }
  }

  function toggleLogVisibility() {
    if (logsContainer.style.display === "none" || logsContainer.style.display === "") {
      logsContainer.style.display = "block";
      buttonIcon.classList.remove("fa-eye-slash");
      buttonIcon.classList.add("fa-eye");
    } else {
      logsContainer.style.display = "none";
      buttonIcon.classList.remove("fa-eye");
      buttonIcon.classList.add("fa-eye-slash");
    }
  }

  document.getElementById("log-btn").addEventListener("click", toggleLogVisibility);
  sendButton.addEventListener("click", handleOutgoingChat);

  chatInput.addEventListener("keypress", (event) => {
    if (event.key === "Enter") {
      event.preventDefault();
      sendButton.click();
    }
  });

  speakButton.addEventListener("click", () => {
    if (isRecording) {
      stopRecording();
    } else {
      startRecording();
    }
  });

  document.addEventListener("keydown", (event) => {
    if (event.code === "Space" && !event.repeat && document.activeElement !== chatInput) {
      event.preventDefault();
      if (!isRecording) startRecording();
    }
  });

  document.addEventListener("keyup", (event) => {
    if (event.code === "Space" && document.activeElement !== chatInput) {
      event.preventDefault();
      if (isRecording) stopRecording();
    }
  });
});
