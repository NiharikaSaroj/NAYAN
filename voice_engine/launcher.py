import subprocess
import time

from wakeword import wait_for_wakeword

print("==============================")
print("NAYAN Background Launcher")
print("==============================")

electron_path = r"C:\Users\riyaj\Documents\NAYAN\electron"

while True:

    print("\nWaiting for wake word...")
    print("Say: Hey Jarvis")

    # Block until wake word is detected
    wait_for_wakeword()

    print("\nWake word detected!")
    print("Opening NAYAN...")

    process = subprocess.Popen(
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

    # Wait until Electron exits
    process.wait()

    print("\nConversation ended.")
    print("Returning to wake-word mode...\n")

    # Small delay before listening again
    time.sleep(2)