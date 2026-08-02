import os
import time

import numpy as np
import sounddevice as sd
import soundfile as sf

SAMPLE_RATE = 16000
CHANNELS = 1

SILENCE_THRESHOLD = 0.005
SILENCE_DURATION = 1.5
MAX_RECORD_TIME = 20

# Prevent hearing our own TTS
MIC_START_DELAY = 0.8

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def record_audio(filename="user_input.wav"):

    filename = os.path.join(BASE_DIR, filename)

    # Wait for speaker playback to completely finish
    time.sleep(MIC_START_DELAY)

    print("Listening...")

    audio_data = []

    speech_started = False
    silence_start = None

    # Start counting timeout only after speech begins
    wait_start = time.time()

    # Ignore first few microphone frames
    warmup_frames = 5
    frame_count = 0

    def callback(indata, frames, time_info, status):

        nonlocal frame_count

        if status:
            return

        frame_count += 1

        # Skip initial noisy frames
        if frame_count <= warmup_frames:
            return

        audio_data.append(indata.copy())

    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype="float32",
        callback=callback,
    ):

        while True:

            time.sleep(0.05)

            # Timeout waiting for user
            if not speech_started:

                if time.time() - wait_start > MAX_RECORD_TIME:
                    print("Recording timeout")
                    break

            if not audio_data:
                continue

            current_chunk = audio_data[-1]

            volume = np.sqrt(np.mean(current_chunk ** 2))

            if volume > SILENCE_THRESHOLD:

                speech_started = True
                silence_start = None

            elif speech_started:

                if silence_start is None:

                    silence_start = time.time()

                elif time.time() - silence_start >= SILENCE_DURATION:

                    break

    if not audio_data:
        return None

    audio = np.concatenate(audio_data, axis=0)

    rms = np.sqrt(np.mean(audio ** 2))

    print(f"Audio volume: {rms:.6f}")

    if rms < 0.003:

        print("No real speech detected")

        return None

    sf.write(
        filename,
        audio,
        SAMPLE_RATE
    )

    print(f"Recording saved: {filename}")

    return filename