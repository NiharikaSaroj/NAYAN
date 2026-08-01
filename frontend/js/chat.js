const input = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");
const micBtn = document.getElementById("micBtn");

const assistantStatus = document.getElementById("assistantStatus");
const statusIcon = document.getElementById("statusIcon");
const statusTitle = document.getElementById("statusTitle");
const statusSubtitle = document.getElementById("statusSubtitle");
const statusText = document.getElementById("statusText");
const statusDot = document.getElementById("statusDot");

const welcomeScreen = document.getElementById("welcomeScreen");

/* =========================================
   Hide Welcome Screen
========================================= */

function hideWelcomeScreen() {

    if (!welcomeScreen)
        return;

    if (welcomeScreen.classList.contains("hidden"))
        return;

    welcomeScreen.classList.add("hidden");

}

/* =========================================
   Assistant State
========================================= */

function setAssistantState(state) {

    micBtn.classList.remove(
        "idle",
        "listening",
        "thinking",
        "speaking"
    );

    micBtn.classList.add(state);

    if (!statusText || !statusDot)
        return;

    switch (state) {

        case "listening":

            statusText.textContent = "Listening";
            statusDot.style.background = "#06B6D4";

            break;

        case "thinking":

            statusText.textContent = "Thinking";
            statusDot.style.background = "#F59E0B";

            break;

        case "speaking":

            statusText.textContent = "Speaking";
            statusDot.style.background = "#8B5CF6";

            break;

        case "starting":

            statusDot.className = "status-dot starting";

            statusText.textContent = "Preparing microphone...";

            break;

        default:

            statusText.textContent = "Ready";
            statusDot.style.background = "#10B981";

    }

}

/* =========================================
   Send Message
========================================= */

async function sendMessage() {

    const message = input.value.trim();

    if (!message)
        return;

    hideWelcomeScreen();

    addUserMessage(message);

    input.value = "";

    setAssistantState("thinking");

    showTyping();

    try {

        const answer = await askNayan(message);

        removeTyping();

        addAIMessage(answer);

        scrollToBottom();

        setAssistantState("idle");

    }

    catch (error) {

        console.error(error);

        removeTyping();

        addAIMessage(
            "Sorry, I could not connect to NAYAN backend."
        );

        scrollToBottom();

        setAssistantState("idle");

    }

}

/* =========================================
   Button Events
========================================= */

sendBtn.addEventListener(
    "click",
    sendMessage
);

micBtn.addEventListener(
    "click",
    async () => {

        hideWelcomeScreen();

        setAssistantState("starting");

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

/* =========================================
   Electron Voice Events
========================================= */

window.electronAPI.onVoiceMessage((data) => {

    /* ---------- Assistant State ---------- */

    if (data.role === "state") {

        if (data.text === "thinking") {

            showTyping();

        }

        setAssistantState(data.text);

        return;

    }

    /* ---------- User Speech ---------- */

    if (data.role === "user") {

        hideWelcomeScreen();

        addUserMessage(data.text);

        scrollToBottom();

        return;

    }

    /* ---------- Assistant Response ---------- */

    if (data.role === "assistant") {

        hideWelcomeScreen();

        removeTyping();

        addAIMessage(data.text);

        scrollToBottom();

        return;

    }

});

/* =========================================
   Initial State
========================================= */

setAssistantState("idle");

