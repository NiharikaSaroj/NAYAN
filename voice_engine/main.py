from wakeword import wait_for_wakeword
from recorder import record_audio
from stt import speech_to_text


def start_nayan():

    print("\n====================")
    print("NAYAN Voice Assistant")
    print("====================\n")


    while True:

        # 1. Wait for wake word
        wait_for_wakeword()


        # 2. Record question
        audio_file = record_audio(
            filename="user_input.wav",
            duration=15
        )


        # 3. Convert speech to text
        text = speech_to_text(audio_file)


        print("\nUser said:")
        print(text)


        print("\nWaiting again...\n")



if __name__ == "__main__":
    start_nayan()