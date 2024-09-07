# FaceChat: Real-Time Emotion-Driven Text-to-Face Animation
FaceChat integrates emotion-driven text analysis with real-time facial animation. User input is processed using sentiment analysis model, and the output is converted into natural speech with OpenAI and ElevenLabs TTS APIs. The speech is then streamed to Audio2Face, which generates corresponding facial animations in real-time, displayed on a website via WebRTC.

While chatbots are widely used with the development of Artificial Intelligence, face-to-face interactions through AI are still emerging. FaceChat is developed to fill this gap. Originally designed to support seniors who find it challenging to read large amounts of text or adapt to fast-changing technologies, FaceChat also aims to provide emotional support to individuals facing loneliness in modern days. While still in its early stages, FaceChat explores the potential of a face-to-face conversational AI service in fields like healthcare, customer service, and entertainment.


## Demo
[Link to Video Demo](https://www.youtube.com/watch?v=jsKBskNUAYM)

[![text_demo](https://github.com/user-attachments/assets/39155820-a99e-44c1-89a7-0098ed3260a1)](https://www.youtube.com/watch?v=jsKBskNUAYM)


## Features
FaceChat combines advanced emotion-driven text analysis with real-time facial animation for an immersive communication experience.

1. **Text Input**: Users can type messages directly into the chatbox.

2. **Voice Input**: Allows voice interaction by clicking the microphone icon or holding the Space bar to start and stop recording.
    ![voice](https://github.com/user-attachments/assets/9eaeb275-b00c-4c4e-b914-2c765c92b187)

3. **Speech to Text**: Converts user voice input into text using OpenAI Speech-to-Text functionality and inserts it into the chatbox.

4. **User Input Submission**: A Send button or pressing Enter sends user inputs to the fine-tuned OpenAI Assistants API.
    ![send](https://github.com/user-attachments/assets/95ac17a4-d6a0-4ab4-a5eb-6f0b503e117d)

5. **Chat Log**: Displays the chat history in the top-left corner. Users can toggle it on or off using the visibility button.

    ![log_demo](https://github.com/user-attachments/assets/15e41699-f049-4181-9306-e4c69fc44264)
    
5. **Sentiment Analysis**: The response is analyzed using a sentiment analysis model developed from Google’s GoEmotions dataset, evaluating its emotional tone.

6. **Natural Speech**: The analyzed text is converted into natural-sounding speech using the ElevenLabs TTS (Text-to-Speech) API.

7. **Facial Animation**: The generated speech chunks are sent to the Audio2Face streaming player, which creates corresponding facial animations in real-time.

8 **WebRTC Streaming**: The animations are displayed on a website via WebRTC, providing a seamless and interactive user experience.


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
- **ML Model Development**: Develop a custom Audio2Human ML model similar to Audio2Face, trained on large video datasets.
- **Cloud Deployment**: Deploy the application on the cloud to increase accessibility and scalability.


## License
This project is licensed under the MIT License - see the LICENSE file for details.
