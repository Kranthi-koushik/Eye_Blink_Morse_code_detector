import cv2
import mediapipe as mp
import time

# Morse code dictionary
MORSE_CODE_DICT = {
    '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E',
    '..-.': 'F', '--.': 'G', '....': 'H', '..': 'I', '.---': 'J',
    '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O',
    '.--.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T',
    '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y',
    '--..': 'Z',
    '-----': '0', '.----': '1', '..---': '2', '...--': '3',
    '....-': '4', '.....': '5', '-....': '6', '--...': '7',
    '---..': '8', '----.': '9'
}

# Mediapipe face mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

# EAR (Eye Aspect Ratio) function
def get_eye_aspect_ratio(landmarks, eye_indices, w, h):
    from math import dist
    p1 = (landmarks[eye_indices[0]].x * w, landmarks[eye_indices[0]].y * h)
    p2 = (landmarks[eye_indices[1]].x * w, landmarks[eye_indices[1]].y * h)
    p3 = (landmarks[eye_indices[2]].x * w, landmarks[eye_indices[2]].y * h)
    p4 = (landmarks[eye_indices[3]].x * w, landmarks[eye_indices[3]].y * h)
    p5 = (landmarks[eye_indices[4]].x * w, landmarks[eye_indices[4]].y * h)
    p6 = (landmarks[eye_indices[5]].x * w, landmarks[eye_indices[5]].y * h)

    # distances
    vertical1 = dist(p2, p6)
    vertical2 = dist(p3, p5)
    horizontal = dist(p1, p4)

    ear = (vertical1 + vertical2) / (2.0 * horizontal)
    return ear

# Eye landmarks
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

# Blink detection thresholds
BLINK_THRESHOLD = 0.23
DOT_DASH_THRESHOLD = 0.3   # <0.3 sec = dot, >=0.3 sec = dash
LETTER_BREAK = 1.2
WORD_BREAK = 2.5

# Variables
blink_start = None
current_symbol = ""
current_sequence = ""
decoded_message = ""
last_blink_time = time.time()

# Webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    h, w, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:
        landmarks = results.multi_face_landmarks[0].landmark

        left_ear = get_eye_aspect_ratio(landmarks, LEFT_EYE, w, h)
        right_ear = get_eye_aspect_ratio(landmarks, RIGHT_EYE, w, h)
        avg_ear = (left_ear + right_ear) / 2.0

        current_time = time.time()

        # Detect blink
        if avg_ear < BLINK_THRESHOLD:
            if blink_start is None:
                blink_start = current_time
        else:
            if blink_start is not None:
                blink_duration = current_time - blink_start
                if blink_duration < DOT_DASH_THRESHOLD:
                    current_sequence += "."
                    print("· Dot")
                else:
                    current_sequence += "-"
                    print("– Dash")
                blink_start = None
                last_blink_time = current_time

        # Check for letter / word breaks
        if current_sequence and (current_time - last_blink_time) > LETTER_BREAK:
            if current_sequence in MORSE_CODE_DICT:
                letter = MORSE_CODE_DICT[current_sequence]
                decoded_message += letter
                print(f" Letter decoded: {letter}")
            else:
                print(" Invalid Morse sequence")
            current_sequence = ""

        if decoded_message and (current_time - last_blink_time) > WORD_BREAK:
            decoded_message += " "
            print("Space added (word break)")

    # Show live feed with decoded message
    cv2.putText(frame, f"Message: {decoded_message}", (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("Blink Morse Code", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC key
        break

cap.release()
cv2.destroyAllWindows()

print("\n Final Decoded Message:", decoded_message)

# Save to file
with open("decoded_message.txt", "w") as f:
    f.write(decoded_message)

print(" Message saved to decoded_message.txt")

