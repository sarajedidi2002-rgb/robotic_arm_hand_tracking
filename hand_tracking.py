#Code test_caméra 

import cv2

# Try opening the default camera (index 0)
cap = cv2.VideoCapture(0)
# Check if the camera opened successfully

if not cap.isOpened():
print("Error: Could not open camera.")
exit()

while True:
# Read a frame from the camera
ret, frame = cap.read()

# If the frame was read successfully
if ret:
# Display the frame in a window
cv2.imshow("Camera Feed", frame)

# Wait for a key press (1 millisecond)
# If the 'q' key is pressed, break the loop
if cv2.waitKey(1) & 0xFF == ord('q'):
break
else:
print("Error: Could not read frame.")
break
# Release the camera and destroy all windows
cap.release()
cv2.destroyAllWindows()


#Code hand _traking

import cv2
import mediapipe as mp
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, # For video
stream max_num_hands=1,
min_detection_confidence=0.7,
min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)
if not cap.isOpened():
print("Error: Could not open camera.")
exit()
while True:
success, image = cap.read()
if not success:
print("Ignoring empty camera frame.")
continue
# Flip the image horizontally for a later selfie-view display
image = cv2.flip(image, 1)
# Convert the BGR image to RGB.
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
# Process the image and get the hand landmarks
results = hands.process(image_rgb)
# Draw the hand landmarks on the image
if results.multi_hand_landmarks:
for hand_landmarks in results.multi_hand_landmarks:
mp_drawing.draw_landmarks(image, hand_landmarks,
mp_hands.HAND_CONNECTIONS)
# Display the image with landmarks
cv2.imshow('Hand Tracking', image)
if cv2.waitKey(5) & 0xFF == ord('q'):
break
hands.close()
cap.release()
cv2.destroyAllWindows()



#Code are fingers up or down 

import cv2
import mediapipe as mp
# Initialize MediaPipe Hands and Drawing modules
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
# Initialize video capture
cap = cv2.VideoCapture(0)
# Define finger tips indices
FINGER_TIPS = [4, 8, 12, 16, 20] # Thumb, Index, Middle, Ring, Pinky
FINGER_NAMES = ["Thumb", "Index", "Middle", "Ring", "Pinky"]
# Setup MediaPipe hands
with mp_hands.Hands(
static_image_mode=False,
max_num_hands=1,
min_detection_confidence=0.7,
min_tracking_confidence=0.7
) as hands:
while True:
ret, frame = cap.read()
if not ret:
break
# Flip and convert the image
frame = cv2.flip(frame, 1)
rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
# Process the frame
result = hands.process(rgb_frame)
if result.multi_hand_landmarks:
for hand_landmarks in result.multi_hand_landmarks:
mp_drawing.draw_landmarks(
frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
# Get landmark coordinates
landmarks = hand_landmarks.landmark
h, w, _ = frame.shape
fingers_status = []
# Thumb: compare x of tip and x of joint
if landmarks[FINGER_TIPS[0]].x < landmarks[FINGER_TIPS[0] - 1].x:
fingers_status.append(1) # Up
else:
fingers_status.append(0) # Down
# Other fingers: compare y of tip and y of joint (one landmark down)
for tip_id in FINGER_TIPS[1:]:
if landmarks[tip_id].y < landmarks[tip_id - 2].y:
fingers_status.append(1)
else:
fingers_status.append(0)
# Display result
for i in range(5):
status = "Up" if fingers_status[i] else "Down"
cv2.putText(frame, f"{FINGER_NAMES[i]}: {status}", (10, 30 + i * 30),
cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0)
if fingers_status[i]
else ((0, 0, 255), 2)
# Show the result
cv2.imshow("Are Fingers Up or Down?", frame)
# Break on 'q'
if cv2.waitKey(1) & 0xFF == ord('q'):
break
# Release resources
cap.release()
cv2.destroyAllWindows()



#Code hand-test
import cv2
import mediapipe as mp
import serial
import time
# Initialize serial communication with Arduino
try:
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
time.sleep(2) # Wait for Arduino to reset
except Exception as e:
print("Error connecting to Arduino:", e)
ser = None
# Initialize MediaPipe Hands and Drawing modules
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
# Initialize video capture
cap = cv2.VideoCapture(0)
# Define finger tips indices
FINGER_TIPS = [4, 8, 12, 16, 20] # Thumb, Index, Middle, Ring, Pinky
FINGER_NAMES = ["Thumb", "Index", "Middle", "Ring", "Pinky"]
# Setup MediaPipe hands
with mp_hands.Hands(
static_image_mode=False,
max_num_hands=1,
min_detection_confidence=0.7,
min_tracking_confidence=0.7) as hands:
while True:
ret, frame = cap.read()
if not ret:
break
# Flip and convert the image
frame = cv2.flip(frame, 1)
rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
# Process the frame
result = hands.process(rgb_frame)
if result.multi_hand_landmarks:
for hand_landmarks in result.multi_hand_landmarks:
mp_drawing.draw_landmarks(
frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
# Get landmark coordinates
landmarks = hand_landmarks.landmark
fingers_status = []
# Thumb: compare x of tip and x of joint
if landmarks[FINGER_TIPS[0]].x < landmarks[FINGER_TIPS[0] - 1].x:
fingers_status.append(1)
else:
fingers_status.append(0)
# Other fingers: compare y of tip and y of joint
for tip_id in FINGER_TIPS[1:]:
if landmarks[tip_id].y < landmarks[tip_id - 2].y:
fingers_status.append(1)
else:
fingers_status.append(0)
# Send status over serial
if ser:
data_string = ",".join(map(str, fingers_status)) + "\n"
ser.write(data_string.encode())
# Display result on screen
for i in range(5):
status = "Up" if fingers_status[i] else "Down"
color = (0, 255, 0) if fingers_status[i] else (0, 0, 255)
cv2.putText(frame, f"{FINGER_NAMES[i]}: {status}", (10, 30 + i * 30),
cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
# Show the result
cv2.imshow("Are Fingers Up or Down?", frame)
# Break on 'q'
if cv2.waitKey(1) & 0xFF == ord('q'):
break
# Release resources
cap.release()
cv2.destroyAllWindows()
if ser:
ser.close()
