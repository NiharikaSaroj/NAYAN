import time

from wakeword import wait_for_wakeword
from recorder import record_audio
from stt import speech_to_text
from tts import text_to_speech
from api_client import ask_nayan


EXIT_COMMANDS = [
    "stop",
    "sleep",
    "exit",
    "bye",
    "go to sleep"
]


MAX_IDLE_TIME = 60
REMINDER_INTERVAL = 30


def start_nayan():

    print("\n====================")
    print("NAYAN Voice Assistant")
    print("====================\n")


    while True:

        # Wait for wake word
        wait_for_wakeword()


        print("\nNAYAN activated\n")


        text_to_speech(
            "Yes, I am listening. How can I help you?"
        )

        time.sleep(2)


        # Conversation timers
        conversation_start = time.time()
        last_reminder = time.time()


        while True:


            current_time = time.time()


            idle_time = current_time - conversation_start


            # Reminder every 20 seconds
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

                print(
                    "Returning to wake word mode...\n"
                )

                break



            # Listen for user
            audio_file = record_audio(
                filename="user_input.wav"
            )


            if audio_file is None:

                print(
                    "No speech detected. Waiting again..."
                )

                continue



            text = speech_to_text(audio_file)


            if not text or len(text.strip()) < 3:

                print(
                    "Invalid speech detected"
                )

                continue



            noise_words = [
                "thank you",
                "thanks",
                "you",
                "bye"
            ]


            if text.lower().strip() in noise_words:

                print(
                    "Ignoring possible hallucination"
                )

                continue



            print("\nUser said:")
            print(text)



            # Reset conversation timer
            conversation_start = time.time()
            last_reminder = time.time()



            text_lower = text.lower()



            if any(
                command in text_lower
                for command in EXIT_COMMANDS
            ):

                text_to_speech(
                    "Okay, I will wait for you."
                )

                print(
                    "Sleeping...\n"
                )

                break



            response = ask_nayan(text)


            print("\nNAYAN:")
            print(response)



            text_to_speech(response)


            # Give TTS time to finish
            time.sleep(3)


            # Reset timer after answering
            conversation_start = time.time()
            last_reminder = time.time()



if __name__ == "__main__":

    start_nayan()