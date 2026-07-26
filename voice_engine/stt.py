from faster_whisper import WhisperModel


print("Loading Whisper model...")


model = WhisperModel(
    "small",
    device="cpu",
    compute_type="int8"
)


print("Whisper ready!")


def speech_to_text(audio_file):

    segments, info = model.transcribe(
        audio_file,
        beam_size=5,
        language="en"
    )


    text = ""

    for segment in segments:
        text += segment.text + " "


    return text.strip()



if __name__ == "__main__":

    audio = "user_input.wav"

    result = speech_to_text(audio)

    print("\nYou said:")
    print(result)