import os
from dotenv import load_dotenv
from google import genai
from rag.prompts import SYSTEM_PROMPT
from app.config import LLM_MODEL
from pathlib import Path

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_answer(question: str, context: str) -> str:
    """
    Generate an answer using only the retrieved NCERT context.
    """
    prompt = f"""
NCERT Reference Material:
{context}

Student Question:
{question}

You are an AI tutor for Class 6 students.

Answer ONLY using the NCERT reference material provided above.

Rules:
- Do not use outside knowledge.
- If the answer is not present in the reference, do not guess.
- Use simple Class 6 language.
- Begin directly with the answer.
- Explain the idea clearly.
- Include one simple real-life example whenever appropriate.
- End with exactly three concise key points in bullet form.
- If the reference material does not contain the answer, do not attempt to answer. Let the application handle the fallback.
- Finish by asking:
"Would you like a short quiz on this topic?"
"""

    try:
        response = client.models.generate_content(
            model=LLM_MODEL,
            contents=f"{SYSTEM_PROMPT}\n\n{prompt}"
        )
        return response.text if response.text else "No response generated."

    except Exception as e:
        print(f"Gemini API Error: {e}")
        raise

def generate_general_answer(question: str) -> str:
    """
    Answer using Gemini's general knowledge when the topic
    is not available in the uploaded NCERT knowledge base.
    """

    prompt = f"""
    You are an AI tutor for Class 6 students.

    The student's question was NOT found in the uploaded NCERT knowledge base.

    Answer using accurate general scientific knowledge.

    Rules:
    - Start directly with the answer.
    - Do NOT introduce yourself.
    - Use simple Class 6 language.
    - Keep the answer between 100 and 180 words.
    - Explain the concept clearly.
    - Give one simple real-life example if appropriate.
    - Do NOT mention NCERT inside the explanation.
    - Do NOT invent chapter names.
    - End with exactly this note:

    Note: This explanation is based on general scientific knowledge because this topic is not available in the uploaded NCERT textbook.

    Question:
    {question}
    """

    response = client.models.generate_content(
        model=LLM_MODEL,
        contents=prompt
    )

    return response.text.strip() if response.text else "No response generated."