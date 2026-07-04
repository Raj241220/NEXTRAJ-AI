import cv2

cap = cv2.VideoCapture(0)

print("Press SPACE to capture image")
print("Press Q to quit")

while True:

    ret, frame = cap.read()

    if not ret:
        break

    cv2.imshow("NEXTRAJ Camera", frame)

    key = cv2.waitKey(1)

    # SPACE
    if key == 32:

        cv2.imwrite("captured.jpg", frame)

        print("✅ Image Saved!")

        break

    # Q
    if key == ord("q"):
        break

cap.release()

cv2.destroyAllWindows()