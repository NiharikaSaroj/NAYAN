function addUserMessage(text) {

    const chat = document.getElementById("chatMessages");

    chat.innerHTML += `
    <div class="user-message">

        <div class="message-content">
            <p>${text}</p>
        </div>

        <div class="message-avatar">
            👤
        </div>

    </div>
    `;

    scrollToBottom();

}

function addAIMessage(text) {

    const chat = document.getElementById("chatMessages");
    const messageId = "msg_" + Date.now();
    chat.innerHTML += `
    <div class="ai-message">

        <div class="message-avatar">
            🤖
        </div>

        <div class="message-content">

            <h6>NAYAN</h6>

            <p id="${messageId}">${text}</p>

            <div class="message-actions">

                <button
                    class="action-btn listen-btn"
                    onclick="listenResponse(this)">

                    <i class="bi bi-volume-up"></i>

                    Listen

                </button>

                <button class="action-btn copy-btn" onclick="copyMessage('${messageId}', this)">

                <button class="action-icon">
                    <i class="bi bi-hand-thumbs-up"></i>
                </button>

                <button class="action-icon">
                    <i class="bi bi-hand-thumbs-down"></i>
                </button>

            </div>

        </div>

    </div>
    `;

    scrollToBottom();

}
function copyMessage(messageId, button) {

    const text = document.getElementById(messageId).innerText;

    navigator.clipboard.writeText(text);

    const original = button.innerHTML;

    button.innerHTML = `
        <i class="bi bi-check2"></i>
        Copied
    `;

    setTimeout(() => {

        button.innerHTML = original;

    }, 1500);

}


function showTyping() {

    if (document.getElementById("typing"))
        return;

    const chat = document.getElementById("chatMessages");

    chat.innerHTML += `
    <div class="ai-message" id="typing">

        <div class="message-avatar">
            🤖
        </div>

        <div class="message-content">

            <h6>NAYAN</h6>

            <p>
                NAYAN is thinking
                <span class="typing-dots">
                    <span>.</span>
                    <span>.</span>
                    <span>.</span>
                </span>
            </p>

        </div>

    </div>
    `;

    scrollToBottom();

}

function removeTyping() {

    const typing =
        document.getElementById("typing");

    if (typing) {
        typing.remove();
    }

    scrollToBottom();

}

function scrollToBottom() {

    const chat =
        document.getElementById("chatMessages");

    if (!chat)
        return;

    chat.scrollTo({

        top: chat.scrollHeight,

        behavior: "smooth"

    });

}
async function listenResponse(button) {

    const message = button
        .closest(".message-content")
        .querySelector("p")
        .innerText;

    button.disabled = true;

    button.innerHTML =
        `<i class="bi bi-volume-up-fill"></i> Speaking...`;

    await window.electronAPI.speakText(message);

    button.disabled = false;

    button.innerHTML =
        `<i class="bi bi-volume-up"></i> Listen`;

}