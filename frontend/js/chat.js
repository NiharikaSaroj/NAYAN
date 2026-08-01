const input = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");
const micBtn = document.getElementById("micBtn");

const assistantStatus = document.getElementById("assistantStatus");
const statusIcon = document.getElementById("statusIcon");
const statusTitle = document.getElementById("statusTitle");
const statusSubtitle = document.getElementById("statusSubtitle");

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

    /* ---------- Future-proof ----------
       If assistantStatus doesn't exist,
       simply animate mic button.
    ----------------------------------- */

    if (!assistantStatus) {

        micBtn.classList.remove(
            "idle",
            "listening",
            "thinking",
            "speaking"
        );

        micBtn.classList.add(state);

        return;

    }

    assistantStatus.className =
        "assistant-status " + state;

    /* Old UI still supported if present */

    if (!statusIcon || !statusTitle || !statusSubtitle)
        return;

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

        default:

            statusIcon.innerHTML = "✨";

            statusTitle.innerHTML = "Ready";

            statusSubtitle.innerHTML =
                "Click the microphone or say Hey NAYAN.";

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

        setAssistantState("idle");

        return;

    }

});

/* =========================================
   Initial State
========================================= */

setAssistantState("idle");

const startupText =
document.getElementById("startupText");

const startupOverlay =
document.getElementById("startupOverlay");

const startupSteps = [

    "Initializing AI...",

    "Loading Voice Engine...",

    "Connecting Knowledge Base...",

    "Preparing Assistant...",

    "Ready"

];

let step = 0;

const interval = setInterval(() => {

    step++;

    if (step < startupSteps.length) {

        startupText.textContent =
            startupSteps[step];

    }

}, 500);

setTimeout(() => {

    clearInterval(interval);

    startupOverlay.classList.add("hidden");

}, 2500);