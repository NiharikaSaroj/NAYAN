from faster_whisper import WhisperModel

# Load the model once when the application starts
# "base" provides a good balance between speed and accuracy.
model = WhisperModel(
    "small",
    device="cpu",
    compute_type="int8"
)

def speech_to_text(audio_path: str) -> str:
    """
    Converts an audio file into text using Faster-Whisper.

    Args:
        audio_path: Path to the audio file.

    Returns:
        Transcribed text.
    """

    segments, info = model.transcribe(
        audio_path,
        beam_size=5,
        language="en"
    )
    text = ""

    for segment in segments:
        text += segment.text + " "

    return text.strip()