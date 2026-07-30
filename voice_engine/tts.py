import subprocess
import sounddevice as sd
import soundfile as sf
import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL = os.path.join(
    BASE_DIR,
    "en_US-lessac-medium.onnx"
)


def play_audio(filename):

    audio, samplerate = sf.read(filename)

    sd.play(
        audio,
        samplerate
    )

    sd.wait()



def text_to_speech(text):
    # Remove markdown symbols for speech
    text = re.sub(r'[*_#`]', '', text)

    output_file = os.path.join(
        BASE_DIR,
        "response.wav"
    )


    command = [
        "piper",
        "--model",
        MODEL,
        "--output_file",
        output_file
    ]


    process = subprocess.Popen(
        command,
        stdin=subprocess.PIPE,
        text=True,
        encoding="utf-8"
    )


    process.communicate(text)


    if process.returncode != 0:

        print("Piper failed")
        return


    print("Generated:", output_file)


    play_audio(output_file)



if __name__ == "__main__":

    text_to_speech(
        "Hello, I am NAYAN. How can I help you?"
    )