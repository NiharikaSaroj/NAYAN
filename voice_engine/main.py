import time

from recorder import record_audio
from stt import speech_to_text
from tts import text_to_speech
from api_client import ask_nayan

EXIT_COMMANDS = {
    "stop",
    "sleep",
    "exit",
    "bye",
    "go to sleep",
    "good bye",
    "goodbye"
}

REPEAT_COMMANDS = {
    "repeat",
    "repeat again",
    "repeat that",
    "repeat it",
    "listen again",
    "say it again",
    "can you repeat",
    "could you repeat",
    "please repeat"
}

NOISE_WORDS = {
    "thank",
    "thanks",
    "thank you",
    "okay",
    "ok",
    "hmm",
    "uh",
    "yes"
}

MAX_IDLE_TIME = 60
REMINDER_INTERVAL = 30

LAST_RESPONSE = None


def reset_idle_timer():
    return time.time(), False


def start_nayan():
    global LAST_RESPONSE

    print("\n====================")
    print("NAYAN Voice Assistant")
    print("====================\n")

    print("Conversation started")

    greeting = "Yes, I am listening. How can I help you today?"

    print("UI_STATE::speaking", flush=True)
    print(f"UI_AI::{greeting}", flush=True)

    text_to_speech(greeting)

    print("UI_STATE::idle", flush=True)

    time.sleep(1)

    conversation_start, reminder_sent = reset_idle_timer()

    while True:

        current_time = time.time()
        idle_time = current_time - conversation_start

        # ---------------------------------
        # 30 second reminder
        # ---------------------------------

        if idle_time >= REMINDER_INTERVAL and not reminder_sent:

            reminder = "Are you still there?"

            print(f"UI_AI::{reminder}", flush=True)
            print("UI_STATE::speaking", flush=True)

            text_to_speech(reminder)

            print("UI_STATE::idle", flush=True)

            reminder_sent = True

            conversation_start = time.time()

        # ---------------------------------
        # 60 second timeout
        # ---------------------------------

        if idle_time >= MAX_IDLE_TIME:

            goodbye = "I am going to sleep now. Call me again when you need me."

            print(f"UI_AI::{goodbye}", flush=True)
            print("UI_STATE::speaking", flush=True)

            text_to_speech(goodbye)

            print("UI_STATE::shutdown", flush=True)

            print("Conversation ended")

            break

        # ---------------------------------
        # Listening
        # ---------------------------------

        print("UI_STATE::listening", flush=True)

        audio_file = record_audio("user_input.wav")

        if audio_file is None:
            continue

        text = speech_to_text(audio_file)

        if not text:
            continue

        text = text.strip()

        if len(text) < 3:
            continue

        print("\nUser said:")
        print(text)

        print(f"UI_USER::{text}", flush=True)

        clean_text = text.lower().strip(".,!? ")

        # User spoke → reset timer
        conversation_start, reminder_sent = reset_idle_timer()

        # ---------------------------------
        # Ignore hallucinations
        # ---------------------------------

        if clean_text in NOISE_WORDS:
            print("Ignoring possible hallucination")
            continue

        # ---------------------------------
        # Repeat
        # ---------------------------------

        if clean_text in REPEAT_COMMANDS:

            if LAST_RESPONSE:

                ui_response = (
                    LAST_RESPONSE
                    .replace("&", "&amp;")
                    .replace("<", "&lt;")
                    .replace(">", "&gt;")
                    .replace("\n", "<br>")
                )

                print(f"UI_AI::{ui_response}", flush=True)
                print("UI_STATE::speaking", flush=True)

                text_to_speech(LAST_RESPONSE)

            else:

                message = "There is no previous answer to repeat."

                print(f"UI_AI::{message}", flush=True)
                print("UI_STATE::speaking", flush=True)

                text_to_speech(message)

            print("UI_STATE::idle", flush=True)

            time.sleep(1)

            conversation_start, reminder_sent = reset_idle_timer()

            continue

        # ---------------------------------
        # Exit
        # ---------------------------------

        if clean_text in EXIT_COMMANDS:

            farewell = "Okay, I will wait for you."

            print(f"UI_AI::{farewell}", flush=True)
            print("UI_STATE::speaking", flush=True)

            text_to_speech(farewell)

            print("UI_STATE::shutdown", flush=True)

            print("Conversation ended")

            break

        # ---------------------------------
        # Thinking
        # ---------------------------------

        print("UI_STATE::thinking", flush=True)

        response = ask_nayan(text)

        if not response:
            response = "Sorry, I couldn't generate a response."

        LAST_RESPONSE = response

        print("\nNAYAN:")
        print(response)

        ui_response = (
            response
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace("\n", "<br>")
        )

        print(f"UI_AI::{ui_response}", flush=True)

        print("UI_STATE::speaking", flush=True)

        text_to_speech(response)

        print("UI_STATE::idle", flush=True)

        time.sleep(1.2)

        # Start silence timer AFTER speaking
        conversation_start, reminder_sent = reset_idle_timer()


if __name__ == "__main__":
    start_nayan()