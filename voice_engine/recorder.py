import sounddevice as sd
import soundfile as sf
import numpy as np
import time


SAMPLE_RATE = 16000
CHANNELS = 1

SILENCE_THRESHOLD = 0.005
SILENCE_DURATION = 1.5
MAX_RECORD_TIME = 20


def record_audio(filename="user_input.wav"):

    print("Listening...")

    audio_data = []

    silence_start = None
    speech_started = False
    start_time = time.time()


    def callback(indata, frames, time_info, status):

        audio_data.append(indata.copy())


    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype="float32",
        callback=callback
    ):

        while True:

            time.sleep(0.1)


            # Maximum waiting time
            if time.time() - start_time > MAX_RECORD_TIME:
                print("Recording timeout")
                break


            if len(audio_data) > 0:

                volume = np.linalg.norm(audio_data[-1])


                if volume > SILENCE_THRESHOLD:

                    speech_started = True
                    silence_start = None

                elif speech_started:

                    if silence_start is None:
                        silence_start = time.time()

                    elif time.time() - silence_start > SILENCE_DURATION:
                        break

    if len(audio_data) == 0:
        return None


    audio = np.concatenate(audio_data, axis=0)
    # Check actual audio energy
    volume = np.sqrt(np.mean(audio ** 2))

    print("Audio volume:", volume)


    # Ignore silent recordings
    if volume < 0.003:
        print("No real speech detected")
        return None


    # Reject empty/silent recordings
    volume = np.linalg.norm(audio) / len(audio)


    sf.write(
        filename,
        audio,
        SAMPLE_RATE
    )


    print("Recording saved:", filename)

    return filename