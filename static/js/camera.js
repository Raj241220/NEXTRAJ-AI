// ======================================
// NEXTRAJ Camera AI
// ======================================

const video = document.getElementById("video");
const canvas = document.getElementById("canvas");
const answer = document.getElementById("answer");

let stream = null;

// ======================================
// Start Camera
// ======================================

async function startCamera() {

    try {

        stream = await navigator.mediaDevices.getUserMedia({

            video: {
                facingMode: "environment"
            },

            audio: false

        });

        video.srcObject = stream;

        answer.innerHTML = "✅ Camera Started";

    }

    catch (err) {

        answer.innerHTML =
            "❌ Unable to access camera.";

        console.log(err);

    }

}

// ======================================
// Speak
// ======================================

function speak(text) {

    speechSynthesis.cancel();

    const speech = new SpeechSynthesisUtterance(text);

    speech.lang = "en-US";

    speech.rate = 1;

    speech.pitch = 1;

    speechSynthesis.speak(speech);

}
// ======================================
// Capture Image
// ======================================

async function captureImage() {

    if (!stream) {

        answer.innerHTML =
            "❌ Please start the camera first.";

        return;

    }

    const context = canvas.getContext("2d");

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    context.drawImage(
        video,
        0,
        0,
        canvas.width,
        canvas.height
    );

    answer.innerHTML = "🤖 Analyzing image...";

    const imageData = canvas.toDataURL("image/jpeg");

    try {

        const response = await fetch("/camera-ai", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({

                image: imageData

            })

        });

        const data = await response.json();

        answer.innerHTML =
            "<b>🤖 AI:</b><br><br>" + data.reply;

        speak(data.reply);

    }

    catch (err) {

        console.log(err);

        answer.innerHTML =
            "❌ Failed to analyze image.";

    }

}
// ======================================
// Auto Start Camera
// ======================================

window.onload = () => {

    startCamera();

};

// ======================================
// Stop Camera on Exit
// ======================================

window.onbeforeunload = () => {

    if (stream) {

        stream.getTracks().forEach(track => {

            track.stop();

        });

    }

};

// ======================================
// Optional: Press Space to Capture
// ======================================

document.addEventListener("keydown", function(event) {

    if (event.code === "Space") {

        event.preventDefault();

        captureImage();

    }

});