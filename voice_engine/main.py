import time

from recorder import record_audio
from stt import speech_to_text
from tts import text_to_speech
from api_client import ask_nayan

EXIT_COMMANDS = [
    "stop",
    "sleep",
    "exit",
    "bye",
    "go to sleep",
    "good bye",
    "goodbye"
]

MAX_IDLE_TIME = 60
REMINDER_INTERVAL = 30


def start_nayan():

    print("\n====================")
    print("NAYAN Voice Assistant")
    print("====================\n")

    print("Conversation started")

    greeting = "Yes, I am listening. How can I help you today?"

    print("UI_STATE::speaking", flush=True)

    print(
        f"UI_AI::{greeting}",
        flush=True
    )

    text_to_speech(greeting)

    print("UI_STATE::listening", flush=True)

    conversation_start = time.time()
    last_reminder = time.time()

    while True:

        current_time = time.time()
        idle_time = current_time - conversation_start

        # Reminder after 30 seconds
        if (
            current_time - last_reminder >= REMINDER_INTERVAL
            and idle_time < MAX_IDLE_TIME
        ):

            text_to_speech(
                "Are you still there?"
            )

            print("Reminder sent")

            last_reminder = current_time

        # Sleep after 60 seconds
        if idle_time >= MAX_IDLE_TIME:

            text_to_speech(
                "I am going to sleep now. Call me again when you need me."
            )

            print("UI_STATE::idle", flush=True)

            print("Conversation ended")

            break

        print("UI_STATE::listening", flush=True)

        audio_file = record_audio(
            filename="user_input.wav"
        )

        if audio_file is None:

            print("No speech detected...")

            continue

        text = speech_to_text(audio_file)

        if not text or len(text.strip()) < 3:

            print("Invalid speech detected")

            continue

        noise_words = [

            "thank you",
            "thanks",
            "thank",
            "bye",
            "goodbye",
            "okay",
            "ok",
            "hmm",
            "uh",
            "yes"

        ]

        if text.lower().strip() in noise_words:

            print("Ignoring possible hallucination")

            continue

        print("\nUser said:")
        print(text)

        print(f"UI_USER::{text}", flush=True)

        conversation_start = time.time()
        last_reminder = time.time()

        text_lower = text.lower()

        # -------------------------------
        # Exit Commands
        # -------------------------------
        if any(
            command in text_lower
            for command in EXIT_COMMANDS
        ):

            farewell = "Okay, I will wait for you."

            # Show farewell in chat
            print(f"UI_AI::{farewell}", flush=True)

            # Speaking animation
            print("UI_STATE::speaking", flush=True)

            text_to_speech(farewell)

            print("UI_STATE::idle", flush=True)

            print("Sleeping...")

            break

        # -------------------------------
        # Normal AI Query
        # -------------------------------
        print("UI_STATE::thinking", flush=True)

        response = ask_nayan(text)

        print("\nNAYAN:")
        print(response)

        ui_response = (
            response
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace("\n", "<br>")
        )

        print("UI_STATE::speaking", flush=True)

        print(
            f"UI_AI::{ui_response}",
            flush=True
        )

        text_to_speech(response)

        print("UI_STATE::idle", flush=True)

        

        # Small pause to avoid hearing its own voice
        time.sleep(1.2)

        conversation_start = time.time()
        last_reminder = time.time()


if __name__ == "__main__":

    start_nayan()