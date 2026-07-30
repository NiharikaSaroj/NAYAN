const input = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");
const micBtn = document.getElementById("micBtn");

const assistantStatus =
    document.getElementById("assistantStatus");

const statusIcon =
    document.getElementById("statusIcon");

const statusTitle =
    document.getElementById("statusTitle");

const statusSubtitle =
    document.getElementById("statusSubtitle");

function setAssistantState(state) {

    assistantStatus.className =
        "assistant-status " + state;

    switch (state) {

        case "listening":

            statusIcon.innerHTML = "🎤";

            statusTitle.innerHTML = "Listening...";

            statusSubtitle.innerHTML =
                "I'm ready for your question.";

            break;

        case "thinking":

            statusIcon.innerHTML = "🧠";

            statusTitle.innerHTML = "Thinking...";

            statusSubtitle.innerHTML =
                "Let me find the best answer.";

            break;

        case "speaking":

            statusIcon.innerHTML = "🔊";

            statusTitle.innerHTML = "Speaking...";

            statusSubtitle.innerHTML =
                "Here's what I found.";

            break;

        case "idle":

            statusIcon.innerHTML = "💤";

            statusTitle.innerHTML = "Ready";

            statusSubtitle.innerHTML =
                "Click the microphone or say Hey Jarvis.";

            break;

    }

}

async function sendMessage() {

    const message = input.value.trim();

    if (message === "")
        return;

    addUserMessage(message);

    input.value = "";

    setAssistantState("thinking");

    showTyping();

    try {

        const answer = await askNayan(message);

        removeTyping();

        addAIMessage(answer);

        setAssistantState("idle");

    }
    catch (error) {

        console.error(error);

        removeTyping();

        addAIMessage(
            "Sorry, I could not connect to NAYAN backend."
        );

        setAssistantState("idle");

    }

}

sendBtn.addEventListener(
    "click",
    sendMessage
);

micBtn.addEventListener(
    "click",
    async () => {

        setAssistantState("listening");

        await window.electronAPI.startVoiceChat();

    }
);

input.addEventListener(
    "keydown",
    function (e) {

        if (e.key === "Enter")
            sendMessage();

    }
);

window.electronAPI.onVoiceMessage((data) => {

    // Assistant state updates
    if (data.role === "state") {

        if (data.text === "thinking") {

            showTyping();

        }

        setAssistantState(data.text);

        return;

    }

    // User speech
    if (data.role === "user") {

        addUserMessage(data.text);

        return;

    }

    // AI streaming response
    if (data.role === "assistant") {

        removeTyping();

        addAIMessage(data.text);

        scrollToBottom();

        return;

    }

});

setAssistantState("idle");