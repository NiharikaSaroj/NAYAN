from rag.retriever import search
from rag.llm import generate_answer


def ask_question(question: str):
    results = search(question)

    context = "\n\n".join([r["text"] for r in results])

    answer = generate_answer(question, context)

    return {
        "answer": answer,
        "sources": list(set([r["source"] for r in results]))
    }