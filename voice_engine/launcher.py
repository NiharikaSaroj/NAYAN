import time
import subprocess
import os

from wakeword import wait_for_wakeword


print("==============================")
print("NAYAN Background Launcher")
print("==============================")

print("\nWaiting for wake word...")
print("Say: Hey Jarvis")


# Wait until wake word detected
wait_for_wakeword()


print("\nWake word detected!")
print("Opening NAYAN...")


# Path to electron folder
electron_path = r"C:\Users\riyaj\Documents\NAYAN\electron"


# Start Electron app
subprocess.Popen(
    [
        "npm",
        "start",
        "--",
        "--wake"
    ],
    cwd=electron_path,
    shell=True
)


print("NAYAN opened")


while True:
    time.sleep(1)