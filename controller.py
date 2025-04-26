import cv2


cap = cv2.VideoCapture(1)  # Replace 0 with 1, 2, etc., if 0 doesn't work

if not cap.isOpened():
    print("❌ Could not open OBS Virtual Camera. Try a different index (0, 1, 2, etc.).")
    exit()

print("✅ OBS Virtual Camera connected successfully!")

while True:
    success, frame = cap.read()
    if not success:
        print("❌ Failed to grab frame from OBS Virtual Camera.")
        break

    # Display the video feed
    cv2.imshow("OBS Virtual Camera Feed", frame)

    # Exit the loop when 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()