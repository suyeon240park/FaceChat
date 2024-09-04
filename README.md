# FaceChat
FaceChat is an advanced AI-driven application that integrates chatbot functionality, text-to-speech (TTS), and real-time facial animation, leveraging NVIDIA's Audio2Face technology. This comprehensive pipeline allows users to interact with an AI chatbot through text or voice, with responses visualized via synchronized facial animation. Designed to enhance emotional support, FaceChat is particularly beneficial for individuals experiencing loneliness and for seniors who may find reading text or adapting to fast-changing technologies challenging. The application also has potential applications across diverse industries, including healthcare, customer service, and entertainment.

## Demo
[Link to Video Demo](https://www.youtube.com/watch?v=jsKBskNUAYM&t=27s)

## Features
- Text Input: Users can type messages directly into the chatbox and submit them by pressing Enter.
- Voice Input: Allows voice interaction by clicking the microphone icon or holding the Space bar to start and stop recording
- Speech to Text: Converts user voice input to text components using OpenAI Speech-To-Text functionality and insert them in the chat box.
- User Input Submission: A Send button directs user inputs to the OpenAI Assistants API for processing.
- WebSockets Integration: Utilizes WebSockets to transmit the AI-generated responses from script.js to generate_voice.py for further processing.
- Voice Synthesis: Implements voice generation using a fine-tuned voice model via the ElevenLabs TTS API.
- Real-Time Facial Animation: Sends voice chunks to NVIDIA Audio2Face, which produce natural and synchronized facial animations corresponding to the generated voice.
- WebRTC Streaming: Streams the animated facial model to a locally hosted website using WebRTC, providing real-time visualization of the responses.

## Usage
Clone the Repository:

bash
Copy code
git clone https://github.com/yourusername/FaceChat.git
Install Dependencies:
Follow the installation instructions for required packages and libraries.

Run the Application:
Start the application by following the provided steps in the repository.

Interact with FaceChat:
Choose between text or voice input and observe the real-time facial animation on the local web interface.

## Future Enhancements
- Enhanced Mesh Model: Implement a more human-like model with improved background and lighting to create a natural and immersive conversational experience.
- Full-Body Animation: Incorporate head movements and full body gestures.
- Custom ML Model Development: Develop a machine learning model similar to Audio2Face, trained on large video datasets.
- Cloud Deployment: Deploy the application on the cloud to increase accessibility and scalability.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
