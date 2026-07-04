from core.vision import ask_image
import pyttsx3

engine = pyttsx3.init()

image_path = "captured.jpg"

print("🤖 NEXTRAJ is analyzing...")

reply = ask_image(image_path)

print(reply)

engine.say(reply)

engine.runAndWait()