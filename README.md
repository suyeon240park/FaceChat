# FaceChat: Bridging AI Interaction with Real-Time Facial Animation
FaceChat is an advanced AI-driven application that integrates chatbot functionality, text-to-speech (TTS), and real-time facial animation using NVIDIA's Audio2Face technology. This comprehensive pipeline allows users to interact with an AI chatbot through text or voice, with responses visualized via synchronized facial animation.

While chatbots are widely used with the development of Artificial Intelligence, face-to-face interactions through AI are still emerging; FaceChat is developed to address this gap. Originally designed to support seniors who find it challenging to read large amounts of text or adapt to fast-changing technologies, FaceChat also aims to provide emotional support to individuals facing loneliness in modern times. While still in its early stages, FaceChat explores the potential of face-to-face conversational AI in fields like healthcare, customer service, and entertainment.

## Demo
[Link to Video Demo](https://www.youtube.com/watch?v=jsKBskNUAYM&t=27s)

![text_demo](https://github.com/user-attachments/assets/5c88fad8-e42e-4e76-845a-42adf2a46d92)


## Features
1. **Text Input**: Users can type messages directly into the chatbox and submit them by pressing Enter.

2. **Voice Input**: Allows voice interaction by clicking the microphone icon or holding the Space bar to start and stop recording


3. **Speech to Text**: Converts user voice input to text components using OpenAI Speech-To-Text functionality and insert them in the chat box.


4. **User Input Submission**: A Send button directs user inputs to the OpenAI Assistants API for processing.


5. **WebSockets Integration**: Utilizes WebSockets to transmit the AI-generated responses from script.js to generate_voice.py for further processing.

6. **Voice Synthesis**: Implements voice generation using a fine-tuned voice model via the ElevenLabs TTS API.

7. **Real-Time Facial Animation**: Sends voice chunks to NVIDIA Audio2Face, which produce natural and synchronized facial animations corresponding to the generated voice.

8. **WebRTC Streaming**: Streams the animated facial model to a locally hosted website using WebRTC, providing real-time visualization of the responses.

9. **Chat Log**: Displays the chat history in the top-left corner. Users can toggle it on or off using the visibility button.

    ![log_demo](https://github.com/user-attachments/assets/15e41699-f049-4181-9306-e4c69fc44264)


## Usage (Window)
**1. Clone the Repository**<br />
Open the terminal in Visual Studio and run the following command:<br />

```bash
git clone https://github.com/suyeon240park/FaceChat.git
```

**2. Activate the Virtual Environment**<br />
```bash
python -m venv .venv
.venv\Scripts\activate
```

**3. Install Dependencies**<br />
```bash
pip install -r requirements.txt
```

**4. Install NVIDIA Omniverse Launcher**<br />
Download and install it [here](https://www.nvidia.com/en-us/omniverse/).

**5. Install Audio2Face via NVIDIA Omniverse Application**<br />
Follow the installation instructions provided within the Omniverse Application.

**6. Move Files**<br />
- Copy the `backend` folder and replace the `streaming_server` folder in the following directory:<br />
  `C:\Users\{User}\AppData\Local\ov\pkg\audio2face-2023.2.0\exts\omni.audio2face.player\omni\audio2face\player\scripts\streaming_server`<br />
- Copy the `frontend` folder and replace the `web` folder in the following directory:<br />
  `C:\Users\{User}\AppData\Local\ov\pkg\audio2face-2023.2.0\extscache\omni.services.streamclient.webrtc-1.3.8\web`

**7. Open NVIDIA Audio2Face Application**<br />
Set up a streaming model as instructed in the application.

**8. Start the Local Server**<br />
Run the following command to start a local server:<br />
```bash
python -m http.server
```

**9. Interact with FaceChat**<br />
Access the local web interface to interact with the AI model and observe real-time facial animation.



## Future Enhancements
- **Enhanced Mesh Model**: Implement a more human-like model with improved background and lighting to create a natural and immersive conversational experience.
- **Full-Body Animation**: Incorporate head movements and full body gestures.
- **Custom ML Model Development**: Develop a machine learning model similar to Audio2Face, trained on large video datasets.
- **Cloud Deployment**: Deploy the application on the cloud to increase accessibility and scalability.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
