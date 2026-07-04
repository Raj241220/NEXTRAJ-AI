import cv2
import time
import pyttsx3
from core.vision import ask_image

engine = pyttsx3.init()

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera not found!")
    exit()

last_time = 0
last_reply = ""

print("🤖 NEXTRAJ Live AI Started")
print("Press Q to Exit")

while True:

    ret, frame = cap.read()

    if not ret:
        break

    cv2.imshow("NEXTRAJ Live AI", frame)

    current = time.time()

    # Analyze every 5 seconds
    if current - last_time > 5:

        cv2.imwrite("live.jpg", frame)

        try:

            reply = ask_image("live.jpg")

            print("\nAI:", reply)

            # Don't repeat the same sentence
            if reply != last_reply:

                engine.say(reply)
                engine.runAndWait()

                last_reply = reply

        except Exception as e:

            print(e)

        last_time = current

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()