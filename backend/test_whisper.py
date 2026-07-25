from audio.whisper_stt import speech_to_text

audio_file = "sample.aac"   # We'll create this next

text = speech_to_text(audio_file)

print("\nTranscription:\n")
print(text)