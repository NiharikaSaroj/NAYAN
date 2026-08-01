import sys
from tts import text_to_speech

if __name__ == "__main__":

    if len(sys.argv) < 2:
        exit()

    text = " ".join(sys.argv[1:])

    text_to_speech(text)