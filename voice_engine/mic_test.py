import sounddevice as sd
import numpy as np
import time

from openwakeword.model import Model


# Load OpenWakeWord ONNX model
model = Model(
    wakeword_models=["hey_jarvis"],
    inference_framework="onnx"
)


# Audio settings
SAMPLE_RATE = 16000
BLOCK_SIZE = 2560


# Detection settings
last_detection_time = 0
COOLDOWN = 5

detection_count = 0
REQUIRED_DETECTIONS = 2

def callback(indata, frames, callback_time, status):

    global last_detection_time

    if status:
        print(status)


    # Convert microphone audio
    audio = np.frombuffer(
        indata,
        dtype=np.int16
    ).astype(np.float32)


    # Normalize audio
    audio = audio / 32768.0


    # Predict wake word
    prediction = model.predict(audio)


    current_time = time.time()


    for key, score in prediction.items():


        if score > 0.35:

            detection_count += 1

        else:
            detection_count = 0


        if detection_count >= REQUIRED_DETECTIONS:

            if current_time - last_detection_time > COOLDOWN:

                last_detection_time = current_time

                print("\n==========================")
                print("Wake word detected!")
                print(f"Confidence: {score}")
                print("==========================\n")

            detection_count = 0



print("================================")
print("NAYAN Wake Word Engine")
print("================================")
print("Listening...")
print("Say: Hey Jarvis")


with sd.InputStream(
    channels=1,
    samplerate=SAMPLE_RATE,
    dtype="int16",
    blocksize=BLOCK_SIZE,
    callback=callback
):

    while True:
        time.sleep(0.1)