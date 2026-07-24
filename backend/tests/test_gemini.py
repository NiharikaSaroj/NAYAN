import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai

load_dotenv(Path(".env"))

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

for model in [
    "models/gemini-2.5-flash-lite",
    "models/gemini-2.0-flash",
    "models/gemini-flash-latest",
    "models/gemini-2.5-pro",
]:
    try:
        response = client.models.generate_content(
            model=model,
            contents="Hello"
        )
        print(f"✅ Works: {model}")
        print(response.text)
        break
    except Exception as e:
        print(f"❌ {model}")
        print(e)