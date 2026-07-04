import cv2

# Open default webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Camera not found!")
    exit()

print("✅ Camera started. Press Q to exit.")

while True:

    ret, frame = cap.read()

    if not ret:
        print("❌ Failed to read frame")
        break

    cv2.imshow("NEXTRAJ Camera Test", frame)

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()