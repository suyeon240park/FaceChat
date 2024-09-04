// Connect to the websockets server at 8100
const socket = new WebSocket('ws://localhost:8100');

socket.onopen = function() {
    console.log('WebSocket connection opened');
};

socket.onclose = function() {
    console.log('WebSocket connection closed');
};

// Get API key and id from environment variables
const openai_api_key = process.env.API_KEY;
const assistant_id = process.env.ASSISTANT_ID;

// Typical header
const headers = {
    "Content-Type": "application/json",
    "Authorization": `Bearer ${openai_api_key}`,
    "OpenAI-Beta": "assistants=v2"
}

// Define sleep that delays the execution of code
const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

// Define elements in html
const chatInput = document.querySelector(".text-input");
const sendButton = document.querySelector("#send-btn");
const logsContainer = document.querySelector("#logs");
const buttonIcon = document.querySelector('#log-btn i');
const speakButton = document.getElementById('speak-btn');

// Run the script when the initial HTML document has been completely loaded and parsed
document.addEventListener("DOMContentLoaded", () => {
    let threadId = null;
    let isRecording = false;
    let mediaRecorder;
    let audioChunks = [];
    
    // Create a new thread
    const createThread = async () => {
        const THREAD_URL = "https://api.openai.com/v1/threads";

        try {
            const response = await fetch(THREAD_URL, {method: "POST", headers: headers});
            const data = await response.json();
            threadId = data.id;
            console.log("Thread created:", threadId);
        } catch (error) {
            console.error("Error creating thread:", error);
        }
    }

    // Record the user voice and insert it into the chat box
    function startRecording() {
        navigator.mediaDevices.getUserMedia({ audio: true })
            .then(stream => {
                mediaRecorder = new MediaRecorder(stream);
                mediaRecorder.start();
                isRecording = true;

                mediaRecorder.ondataavailable = event => {
                    audioChunks.push(event.data);
                };

                mediaRecorder.onstop = () => {
                    const audioBlob = new Blob(audioChunks, { type: 'audio/mp3' });
                    audioChunks = [];
                    sendToOpenAI(audioBlob);
                };
            })
            .catch(error => {
                console.error('Error accessing the microphone:', error);
            });
        // Generate animation while mic is on
        speakButton.innerHTML = '<div class="speaker_on"></div>';
    }

    function stopRecording() {
        mediaRecorder.stop();
        isRecording = false;

        // Return to the original emoji when mic is off
        speakButton.innerHTML = '<i class="fas fa-microphone"></i>';
    }

    // Send the audio input to OpenAI Speech to Text API
    function sendToOpenAI(audioBlob) {
        const SPEECH_TO_TEXT_URL = 'https://api.openai.com/v1/audio/transcriptions';

        const formData = new FormData();
        formData.append("file", audioBlob);
        formData.append("model", "whisper-1");
        
        fetch(SPEECH_TO_TEXT_URL, {
            method: 'POST',
            headers: {
                "Authorization": `Bearer ${openai_api_key}`
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            console.log(data.text)
            chatInput.value = data.text;
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }

    // Make an API request to the OpenAI Assistants API.
    const getChatResponse = async (userText, threadId) => {
        const MESSAGE_URL = `https://api.openai.com/v1/threads/${threadId}/messages`;
        const RUN_URL = `https://api.openai.com/v1/threads/${threadId}/runs`;
        
        // Create a message in the current thread
        try {
            const response = await fetch(MESSAGE_URL, {
                method: "POST",
                headers: headers,
                body: JSON.stringify({
                    "role": "user",
                    "content": userText
                })
            });
            const data = await response.json();
            console.log("message:", data);
        } catch (error) {
            return "Error creating a message.";
        }

        // Run it
        try {
            let response = await fetch(RUN_URL, {
                method: "POST",
                headers: headers,
                body: JSON.stringify({
                    "assistant_id": assistant_id
                })
            });

            var data = await response.json();

            // Check the run status by retrieving the run object
            while (data.status !== 'completed') {
                console.log('Run Status: ' + data.status);

                if (data.status == 'failed') {
                    return "Run failed";
                }

                let response = await fetch(RUN_URL + `/${data.id}`, {
                    method: "GET",
                    headers: {
                        "Authorization": `Bearer ${openai_api_key}`,
                        "OpenAI-Beta": "assistants=v2"
                    }
                });

                data = await response.json();
                await sleep(200); // Sleep for 200 milliseconds
            }

            console.log('Run Status: ' + data.status);

        } catch (error) {
            console.error('Error checking run status:', error);
        }


        // Get the response
        try {
            const response = await fetch(MESSAGE_URL, {
                method: "GET",
                headers: headers
            });

            const data = await response.json();
            console.log("Response:", data);
            return data.data[0].content[0].text.value;
        } catch (error) {
            console.error("Error fetching response:", error);
            return "Error getting the response.";
        }
    };


    // 
    const handleOutgoingChat = async () => {
        // Get the user's input and trim any whitespace
        const userText = chatInput.value.trim();

        // If the input is empty, log a message and exit the function
        if (!userText) {
            console.log("No user input.");
            return;
        }

        // Clear the chat input field
        chatInput.value = '';

        // Show loading state on the send button
        sendButton.innerHTML = '<div class="loader"></div>';
        sendButton.disabled = true;

        // If the thread hasn't been created yet, create it
        if (!threadId) {
            await createThread();
        }
    
        // Display the user's input in the logs
        const userLog = document.createElement("div");
        userLog.classList.add("logs");
        userLog.innerHTML = `<p><strong>User:</strong> ${userText}</p>`;
        logsContainer.appendChild(userLog);
    
        // Get the response from the API
        const response = await getChatResponse(userText, threadId);
    
        // Send the modified text (for better emotion and speed in tts) to the server when the connection is open
        modified = response.replace(/,/g, " --").replace(/\./g, "...");
        socket.send(modified);

        // Display the bot's response in the logs
        const janeLog = document.createElement("div");
        janeLog.classList.add("logs");
        janeLog.innerHTML = `<p><strong>ori:</strong> ${response}</p>`;
        logsContainer.appendChild(janeLog);

        // Restore the send button to its original state
        sendButton.innerHTML = '<i class="fas fa-paper-plane"></i>';
        sendButton.disabled = false;
    };

    // Function to toggle the visibility of the logs
    const toggleLogVisibility = () => {
        if (logsContainer.style.display === 'none' || logsContainer.style.display === '') {
            logsContainer.style.display = 'block'; // Show logs
            buttonIcon.classList.remove('fa-eye-slash');
            buttonIcon.classList.add('fa-eye');
        } else {
            logsContainer.style.display = 'none'; // Hide logs
            buttonIcon.classList.remove('fa-eye');
            buttonIcon.classList.add('fa-eye-slash');
        }
    };

    
    // Add event listener to the toggle button
    document.getElementById('log-btn').addEventListener('click', toggleLogVisibility);

    // Add event listener to the send button
    sendButton.addEventListener("click", handleOutgoingChat);
    
    // Add event listener to the chat input field
    chatInput.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            event.preventDefault(); // Prevent the default action of adding a new line
            sendButton.click();
        }
    });

    // Add event listener to the speaker button
    speakButton.addEventListener('click', () => {
        if (!isRecording) {
            startRecording();
        } else {
            stopRecording();
        }
    });

    // While pressing the space bar, the program records user's voice
    document.addEventListener('keydown', function (event) {
        if (event.code === 'Space' && !event.repeat) {
            if (document.activeElement !== chatInput) { // If the user is typing, do not trigger mic
                event.preventDefault();
                if (!isRecording) {
                    startRecording();
                }
            }
        }
    });

    // When the user release the space bar, it stops recording
    document.addEventListener('keyup', function (event) {
        if (event.code === 'Space') {
            if (document.activeElement !== chatInput) {
                event.preventDefault();
                if (isRecording) {
                    stopRecording();
                }
            }
        }
    });

});