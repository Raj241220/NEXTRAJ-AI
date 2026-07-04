import os
import base64
import markdown

from io import BytesIO
from PIL import Image

from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename

from core.ai import ask_ai
from core.vision import ask_image
from core.pdf_reader import read_pdf
from core.pdf_memory import save_pdf

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# ==========================
# HOME
# ==========================

@app.route("/")
def home():
    return render_template("index.html")


# ==========================
# CAMERA PAGE
# ==========================

@app.route("/camera")
def camera():
    return render_template("camera.html")


# ==========================
# AI CHAT
# ==========================

@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    message = data.get("message", "").strip()

    if message == "":
        return jsonify({
            "reply": "Please type a message."
        })

    reply = ask_ai(message)

    reply = markdown.markdown(reply)

    return jsonify({
        "reply": reply
    })


# ==========================
# IMAGE AI
# ==========================

@app.route("/image", methods=["POST"])
def image():

    if "image" not in request.files:
        return jsonify({
            "reply": "No image received."
        })

    file = request.files["image"]

    filename = secure_filename(file.filename)

    path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    file.save(path)

    try:

        reply = ask_image(path)

    except Exception as e:

        reply = f"Vision Error: {e}"

    return jsonify({
        "reply": reply
    })


# ==========================
# CAMERA AI
# ==========================

@app.route("/camera-ai", methods=["POST"])
def camera_ai():

    try:

        data = request.get_json()

        image_data = data["image"]

        image_data = image_data.split(",")[1]

        image_bytes = base64.b64decode(image_data)

        image = Image.open(BytesIO(image_bytes))

        temp_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            "camera.jpg"
        )

        image.save(temp_path)

        reply = ask_image(temp_path)

        return jsonify({
            "reply": reply
        })

    except Exception as e:

        return jsonify({
            "reply": f"Camera AI Error: {str(e)}"
        })


# ==========================
# PDF AI
# ==========================

@app.route("/pdf", methods=["POST"])
def pdf():

    if "pdf" not in request.files:
        return jsonify({
            "reply": "No PDF received."
        })

    file = request.files["pdf"]

    filename = secure_filename(file.filename)

    path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    file.save(path)

    try:

        text = read_pdf(path)

        save_pdf(filename, text)

        return jsonify({
            "reply": text[:4000]
        })

    except Exception as e:

        return jsonify({
            "reply": f"PDF Error: {e}"
        })


# ==========================
# RUN SERVER
# ==========================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )