from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
import markdown

from core.ai import ask_ai
from core.vision import ask_image

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    if not data:
        return jsonify({"reply": "Invalid request."})

    message = data.get("message", "").strip()

    if message == "":
        return jsonify({"reply": "Please type a message."})

    reply = ask_ai(message)

    try:
        reply = markdown.markdown(reply)
    except Exception:
        pass

    return jsonify({
        "reply": reply
    })


@app.route("/image", methods=["POST"])
def image():

    if "image" not in request.files:
        return jsonify({
            "reply": "No image uploaded."
        })

    file = request.files["image"]

    if file.filename == "":
        return jsonify({
            "reply": "No image selected."
        })

    filename = secure_filename(file.filename)

    path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    file.save(path)

    try:

        reply = ask_image(path)

    except Exception as e:

        reply = f"Vision Error: {e}"

    return jsonify({
        "reply": reply
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )