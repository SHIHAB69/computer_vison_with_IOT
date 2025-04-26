import cv2
import serial
import time
from cvzone.HandTrackingModule import HandDetector

# Initialize serial communication with Arduino
arduino = serial.Serial('/dev/cu.usbserial-110', 9600)  # Replace with your Arduino port
time.sleep(2)  # Wait for the connection to establish

# Initialize HandDetector
detector = HandDetector(detectionCon=0.8, maxHands=1)

# Open webcam
video = cv2.VideoCapture(1)

def send_command(command):
    """Send command to the Arduino."""
    arduino.write(command.encode())
    print(f"Sent command: {command}")
    time.sleep(0.2)  # Add a small delay to avoid flooding the Arduino with commands

while True:
    ret, frame = video.read()
    frame = cv2.flip(frame, 1)  # Flip the frame horizontally
    hands, img = detector.findHands(frame)  # Detect hands in the frame

    if hands:
        # Get the first detected hand
        lmList = hands[0]
        fingerUp = detector.fingersUp(lmList)  # Get the state of each finger (1 = up, 0 = down)

        print(fingerUp)  # Debugging: Print the finger states

        # Map finger states to commands
        if fingerUp == [0, 0, 0, 0, 0]:  # All fingers down
            send_command('B')  # Backward
            cv2.putText(frame, 'Command: Backward', (20, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
        elif fingerUp == [0, 1, 0, 0, 0]:  # Index finger up
            send_command('R')  # Turn right
            cv2.putText(frame, 'Command: Right', (20, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
        elif fingerUp == [0, 1, 1, 0, 0]:  # Index and middle fingers up
            send_command('L')  # Turn left
            cv2.putText(frame, 'Command: Left', (20, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
        elif fingerUp == [1, 1, 1, 1, 1]:  # All fingers up
            send_command('F')  # Forward
            cv2.putText(frame, 'Command: Forward', (20, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
        elif fingerUp == [1, 0, 0, 0, 0]:  # Thumb up
            send_command('S')  # Stop
            cv2.putText(frame, 'Command: Stop', (20, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)

    # Display the frame
    cv2.imshow("Hand Gesture Control", frame)

    # Exit with 'k' key
    k = cv2.waitKey(1)
    if k == ord("k"):
        break

video.release()
cv2.destroyAllWindows()
arduino.close()
print("Program stopped")