from recorder import record_audio
from stt import speech_to_text
from api_client import ask_nayan
from tts import text_to_speech


def start_voice_chat():

    try:

        # -------------------------------
        # Listening
        # -------------------------------
        print("UI_STATE::listening", flush=True)

        audio = record_audio("user_input.wav")

        if audio is None:
            print("UI_STATE::idle", flush=True)
            return

        text = speech_to_text(audio)

        if not text:
            print("UI_STATE::idle", flush=True)
            return

        # Ignore empty text
        text = text.strip()

        if len(text) == 0:
            print("UI_STATE::idle", flush=True)
            return

        # Show user message
        print(f"UI_USER::{text}", flush=True)

        # -------------------------------
        # Thinking
        # -------------------------------
        print("UI_STATE::thinking", flush=True)

        response = ask_nayan(text)

        if not response:
            response = "Sorry, I couldn't generate a response."

        # Send full response to UI
        ui_response = response.replace("\n", "<br>")

        print(f"UI_AI::{ui_response}", flush=True)

        # -------------------------------
        # Speaking
        # -------------------------------
        print("UI_STATE::speaking", flush=True)

        text_to_speech(response)

        # -------------------------------
        # Back to Ready
        # -------------------------------
        print("UI_STATE::idle", flush=True)

    except Exception as e:

        print("VOICE_CHAT_ERROR:", e, flush=True)

        print("UI_STATE::idle", flush=True)


if __name__ == "__main__":
    start_voice_chat()