// ===============================
// Save & Load Chat
// ===============================

function saveChat() {
    localStorage.setItem(
        "nextraj_chat",
        document.getElementById("chat").innerHTML
    );
}

function loadChat() {

    const oldChat = localStorage.getItem("nextraj_chat");

    if (oldChat) {
        document.getElementById("chat").innerHTML = oldChat;
    }

}

// ===============================
// Typing Animation
// ===============================

async function typeText(element, text, speed = 15) {

    element.innerHTML = "🤖 ";

    for (let i = 0; i < text.length; i++) {

        element.innerHTML += text.charAt(i);

        await new Promise(resolve => setTimeout(resolve, speed));

    }

}

// ===============================
// Chat History
// ===============================

function updateHistory() {

    const history = document.getElementById("history");

    if (!history) return;

    history.innerHTML = "";

    const firstMessage = document.querySelector(".user");

    if (!firstMessage) return;

    const item = document.createElement("div");

    item.className = "history-item";

    let title = firstMessage.innerText;

    if (title.length > 30) {

        title = title.substring(0, 30) + "...";

    }

    item.innerHTML = title;

    history.appendChild(item);

}

// ===============================
// New Chat
// ===============================

function newChat() {

    if (!confirm("Start a new chat?")) return;

    localStorage.removeItem("nextraj_chat");

    document.getElementById("chat").innerHTML = `
        <div class="ai">
            👋 Hello Raj! I am NEXTRAJ.AI.
        </div>
    `;

    updateHistory();

}
// ===============================
// Send Message
// ===============================

async function sendMessage() {

    const input = document.getElementById("message");
    const chat = document.getElementById("chat");

    const message = input.value.trim();

    if (message === "") return;

    // User Message
    chat.innerHTML += `
        <div class="user">
            👤 ${message}
        </div>
    `;

    input.value = "";

    saveChat();

    // Typing Message
    chat.innerHTML += `
        <div class="ai" id="typing">
            🤖 NEXTRAJ.AI is typing...
        </div>
    `;

    chat.scrollTop = chat.scrollHeight;

    try {

        const response = await fetch("/chat", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: message
            })

        });

        const data = await response.json();

        document.getElementById("typing").remove();

        const ai = document.createElement("div");

        ai.className = "ai";

        chat.appendChild(ai);

        const cleanReply = data.reply.replace(/<[^>]*>/g, "");

        await typeText(ai, cleanReply);

        saveChat();

        updateHistory();

        // Voice Output
        const speech = new SpeechSynthesisUtterance(cleanReply);

        speech.lang = "en-US";
        speech.rate = 1;
        speech.pitch = 1;

        window.speechSynthesis.speak(speech);

        chat.scrollTop = chat.scrollHeight;

    }

    catch (err) {

        const typing = document.getElementById("typing");

        if (typing) typing.remove();

        chat.innerHTML += `
            <div class="ai">
                ❌ Error connecting to AI.
            </div>
        `;

    }

}
// ===============================
// Voice Assistant
// ===============================

function startVoice() {

    if (!("webkitSpeechRecognition" in window)) {
        alert("Voice Recognition is not supported in this browser.");
        return;
    }

    const recognition = new webkitSpeechRecognition();

    recognition.lang = "en-US";
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.start();

    recognition.onresult = function(event) {

        const text = event.results[0][0].transcript;

        document.getElementById("message").value = text;

        sendMessage();

    };

}

// ===============================
// Image Upload
// ===============================

async function sendImage() {

    const fileInput = document.getElementById("imageInput");

    if (!fileInput || fileInput.files.length === 0) return;

    const file = fileInput.files[0];

    const chat = document.getElementById("chat");

    // Preview
    const imgURL = URL.createObjectURL(file);

    chat.innerHTML += `
        <div class="user">
            <img src="${imgURL}" style="max-width:250px;border-radius:12px;">
        </div>
    `;

    chat.innerHTML += `
        <div class="ai" id="typing">
            🤖 Looking at image...
        </div>
    `;

    chat.scrollTop = chat.scrollHeight;

    const formData = new FormData();

    formData.append("image", file);

    try {

        const response = await fetch("/image", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        const typing = document.getElementById("typing");
        if (typing) typing.remove();

        const ai = document.createElement("div");
        ai.className = "ai";
        ai.innerHTML = "🤖 " + data.reply;

        chat.appendChild(ai);

        saveChat();

        const speech = new SpeechSynthesisUtterance(data.reply);

        speech.lang = "en-US";

        window.speechSynthesis.speak(speech);

        chat.scrollTop = chat.scrollHeight;

    } catch (err) {

        const typing = document.getElementById("typing");
        if (typing) typing.remove();

        chat.innerHTML += `
            <div class="ai">
                ❌ Image processing failed.
            </div>
        `;

    }

    fileInput.value = "";

}

// ===============================
// Page Load
// ===============================

document.addEventListener("DOMContentLoaded", function () {

    loadChat();

    updateHistory();

    const input = document.getElementById("message");

    input.addEventListener("keypress", function(e){

        if(e.key === "Enter"){
            sendMessage();
        }

    });

    const imageInput = document.getElementById("imageInput");

    if(imageInput){

        imageInput.addEventListener("change", function(){

            if(this.files.length > 0){

                sendImage();

            }

        });

    }

});