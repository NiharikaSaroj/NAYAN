import sounddevice as sd
import soundfile as sf
import time


SAMPLE_RATE = 16000
CHANNELS = 1


def record_audio(
        filename="user_input.wav",
        duration=15
):

    print("Recording started...")

    audio = sd.rec(
        int(duration * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype="float32"
    )

    sd.wait()


    sf.write(
        filename,
        audio,
        SAMPLE_RATE
    )


    print("Recording saved:", filename)


    return filename



if __name__ == "__main__":

    print("Test recorder")

    time.sleep(1)

    record_audio(
        duration=15
    )