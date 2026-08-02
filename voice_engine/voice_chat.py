from recorder import record_audio
from stt import speech_to_text
from api_client import ask_nayan
from tts import text_to_speech

LAST_RESPONSE = None


def start_voice_chat():

    global LAST_RESPONSE

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

        text = text.strip()

        repeat_commands = {
            "repeat",
            "repeat again",
            "repeat that",
            "repeat it",
            "listen again",
            "say it again",
            "can you repeat",
            "could you repeat",
            "please repeat",
        }

        clean_text = text.lower().strip(".,!? ")

        # -------------------------------
        # Repeat Previous Response
        # -------------------------------
        if clean_text in repeat_commands:

            if LAST_RESPONSE is not None:

                print(
                    "UI_AI::"
                    + LAST_RESPONSE["answer"].replace("\n", "<br>"),
                    flush=True,
                )

                print("UI_STATE::speaking", flush=True)

                text_to_speech(LAST_RESPONSE["answer"])

            else:

                message = "There is no previous answer to repeat."

                print(f"UI_AI::{message}", flush=True)
                print("UI_STATE::speaking", flush=True)

                text_to_speech(message)

            print("UI_STATE::idle", flush=True)
            return

        # -------------------------------
        # Show User Message
        # -------------------------------
        print(f"UI_USER::{text}", flush=True)

        # -------------------------------
        # Thinking
        # -------------------------------
        print("UI_STATE::thinking", flush=True)

        response = ask_nayan(text)

        if not response:
            response = "Sorry, I couldn't generate a response."

        LAST_RESPONSE = {
            "question": text,
            "answer": response,
        }

        # -------------------------------
        # Send Response to UI
        # -------------------------------
        print(
            f"UI_AI::{response.replace(chr(10), '<br>')}",
            flush=True,
        )

        # -------------------------------
        # Speaking
        # -------------------------------
        print("UI_STATE::speaking", flush=True)

        text_to_speech(response)

        print("UI_STATE::idle", flush=True)

    except Exception as e:

        print(f"VOICE_CHAT_ERROR: {e}", flush=True)
        print("UI_STATE::idle", flush=True)


if __name__ == "__main__":
    start_voice_chat()