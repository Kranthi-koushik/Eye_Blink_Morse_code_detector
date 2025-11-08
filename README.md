The Eye Blink Morse Code Detector is a hands-free communication system that interprets eye blinks as Morse code using computer vision and Python automation. It leverages MediaPipe FaceMesh and OpenCV to detect and track the user’s eyes in real time through a webcam.

By analyzing the Eye Aspect Ratio (EAR), the system determines when a blink occurs and classifies it based on its duration:

Short blinks are interpreted as dots (·)

Long blinks are interpreted as dashes (–)

The generated Morse sequence is continuously decoded into English letters and words using a Morse code dictionary. The decoded text is displayed live on the video feed and also saved in a text file for later use.

This project demonstrates the integration of computer vision, signal interpretation, and assistive technology, providing an innovative means of communication for individuals with mobility or speech limitations. It can also serve as a foundation for projects in human-computer interaction (HCI), biometric interfaces, and AI-based assistive tools.

🧩 Key Features

👁️ Real-time eye tracking using MediaPipe FaceMesh

⚡ Converts blink durations into Morse code symbols

🔤 Decodes Morse code into text dynamically

💬 Displays decoded message on the webcam feed

💾 Saves the final output to decoded_message.txt

🧠 Adjustable sensitivity thresholds for blink detection

🧠 Working Principle

The system initializes the webcam and detects facial landmarks.

The Eye Aspect Ratio (EAR) is calculated for both eyes.

When the EAR drops below a threshold, a blink is detected.

Blink duration determines if it’s a dot (·) or a dash (–).

Time intervals between blinks define letter or word breaks.

The Morse code sequence is decoded into readable text in real time.

⚙️ Technologies Used

Python

OpenCV – Video capture and frame processing

MediaPipe – Facial landmark detection and tracking

Time module – Blink duration measurement

Morse Code Mapping – Symbol decoding logic

🎯 Applications

Assistive communication for people with ALS, paralysis, or speech disabilities

Human-Computer Interaction (HCI) research

Gesture and facial-based control interfaces

Educational projects in computer vision and signal processing
