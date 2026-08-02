import time
import numpy as np
import sounddevice as sd

from openwakeword.model import Model

SAMPLE_RATE = 16000
CHUNK_SIZE = 1280

WAKEWORD = "hey_jarvis"

# Slightly stricter
THRESHOLD = 0.55

# Require more consecutive detections
REQUIRED_DETECTIONS = 5

# Wait after Electron closes before listening
MIC_SETTLE_TIME = 3

# Wait after a successful wakeword
WAKEWORD_COOLDOWN = 2


def wait_for_wakeword():

    print("Waiting for microphone to settle...")
    time.sleep(MIC_SETTLE_TIME)

    # IMPORTANT:
    # Create a NEW model every time we start listening.
    model = Model(
        wakeword_models=[WAKEWORD],
        inference_framework="onnx"
    )

    print("Listening for wake word...")
    print("Say: Hey Jarvis")

    detection_count = 0
    detected = False

    # Ignore first microphone buffers
    warmup_frames = 10
    frame_counter = 0

    def audio_callback(indata, frames, time_info, status):

        nonlocal detection_count
        nonlocal detected
        nonlocal frame_counter

        if status:
            return

        frame_counter += 1

        if frame_counter <= warmup_frames:
            return

        audio = indata[:, 0]
        audio = (audio * 32767).astype(np.int16)

        prediction = model.predict(audio)

        score = prediction.get(WAKEWORD, 0)

        # Uncomment if you want to debug confidence
        # print(score)

        if score >= THRESHOLD:

            detection_count += 1

        else:

            detection_count = max(0, detection_count - 1)

        if detection_count >= REQUIRED_DETECTIONS:

            print("\n====================")
            print("NAYAN activated!")
            print(f"Confidence: {score:.3f}")
            print("====================\n")

            detected = True
            detection_count = 0

    with sd.InputStream(
        channels=1,
        samplerate=SAMPLE_RATE,
        blocksize=CHUNK_SIZE,
        dtype="float32",
        callback=audio_callback,
    ):

        while not detected:
            time.sleep(0.05)

    # Release model memory completely
    del model

    time.sleep(WAKEWORD_COOLDOWN)

    return True


if __name__ == "__main__":
    wait_for_wakeword()