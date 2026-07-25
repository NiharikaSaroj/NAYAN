import json
from rag.llm import client
from rag.quiz_prompt import QUIZ_PROMPT


def generate_quiz(context):

    prompt = f"""
Context:

{context}
"""

    response = client.models.generate_content(
        model="models/gemini-flash-latest",
        contents=f"{QUIZ_PROMPT}\n\n{prompt}"
    )

    quiz_text = response.text.strip()

    # Remove markdown if Gemini returns ```json ... ```
    if quiz_text.startswith("```json"):
        quiz_text = quiz_text.replace("```json", "").replace("```", "").strip()

    return json.loads(quiz_text)