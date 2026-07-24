import os
from dotenv import load_dotenv
from google import genai
from rag.prompts import SYSTEM_PROMPT

from pathlib import Path

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_answer(question, context):
    prompt = f"""
NCERT Reference Material:
{context}

Student Question:
{question}

Instructions:
- Answer ONLY from the NCERT reference material.
- Explain in simple Class 6 language.
- Give one real-life example if appropriate.
- Summarize the answer in 3 key points.
- End by asking whether the student wants a short quiz.
"""

    try:
        response = client.models.generate_content(
            model="models/gemini-flash-latest",
            contents=f"{SYSTEM_PROMPT}\n\n{prompt}"
        )
        return response.text

    except Exception as e:
        print(e)
        raise