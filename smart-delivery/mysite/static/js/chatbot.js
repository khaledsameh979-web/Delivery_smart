function toggleChat() {
    document.getElementById("chat-window").classList.toggle("hidden");
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(";").shift();
}

async function sendMessage() {
    const input = document.getElementById("chat-input");
    const msg = input.value.trim();
    if (!msg) return;
    input.value = "";

    const box = document.getElementById("chat-messages");
    box.innerHTML += `<div class="user-msg">${msg}</div>`;
    box.scrollTop = box.scrollHeight;

    const res = await fetch("/api/chat/", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: `message=${encodeURIComponent(msg)}`,
    });
    const data = await res.json();

    box.innerHTML += `<div class="bot-msg">${data.reply}</div>`;
    box.scrollTop = box.scrollHeight;
}

document.getElementById("chat-input")?.addEventListener("keydown", (e) => {
    if (e.key === "Enter") sendMessage();
});