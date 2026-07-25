from rag.retriever import search
from rag.quiz import generate_quiz

query = "Food"

results = search(query)

context = "\n\n".join(r["text"] for r in results)

quiz = generate_quiz(context)

print(quiz)