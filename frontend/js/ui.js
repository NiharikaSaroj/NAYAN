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

    chat.innerHTML += `
    <div class="ai-message">

        <div class="message-avatar">
            🤖
        </div>

        <div class="message-content">

            <h6>NAYAN</h6>

            <p>${text}</p>

        </div>

    </div>
    `;

    scrollToBottom();

}

function showTyping() {

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

    const typing = document.getElementById("typing");

    if (typing)
        typing.remove();

}

function scrollToBottom() {

    const chat = document.getElementById("chatMessages");

    chat.scrollTop = chat.scrollHeight;

}