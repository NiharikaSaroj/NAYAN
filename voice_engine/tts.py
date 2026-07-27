import subprocess
import sounddevice as sd
import soundfile as sf


MODEL = "en_US-lessac-medium.onnx"


def play_audio(filename):

    audio, samplerate = sf.read(filename)

    sd.play(audio, samplerate)

    sd.wait()



def text_to_speech(text):

    output_file = "response.wav"


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
        text=True
    )


    process.communicate(text)


    print("Generated:", output_file)


    # Play voice automatically
    play_audio(output_file)



if __name__ == "__main__":

    text_to_speech(
        "Hello, I am NAYAN. How can I help you?"
    )