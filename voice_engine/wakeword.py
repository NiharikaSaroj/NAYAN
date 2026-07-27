import time
import numpy as np
import sounddevice as sd

from openwakeword.model import Model


SAMPLE_RATE = 16000
CHUNK_SIZE = 1280

WAKEWORD = "hey_jarvis"

THRESHOLD = 0.35
REQUIRED_DETECTIONS = 2


model = Model(
    wakeword_models=[WAKEWORD],
    inference_framework="onnx"
)


def wait_for_wakeword():

    print("Listening for wake word...")
    print("Say: Hey Jarvis")

    detection_count = 0
    detected = False


    def audio_callback(indata, frames, time_info, status):

        nonlocal detection_count, detected

        if status:
            if "overflow" in str(status):
                return


        audio = indata[:, 0]

        audio = (audio * 32767).astype(np.int16)


        prediction = model.predict(audio)


        score = prediction.get(WAKEWORD, 0)


        if score > THRESHOLD:
            detection_count += 1
        else:
            detection_count = 0


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
        callback=audio_callback
    ):

        while not detected:
            time.sleep(0.1)


    return True