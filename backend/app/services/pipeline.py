from rag.retriever import search
from rag.llm import generate_answer
from rag.quiz import generate_quiz


def ask_question(question: str):
    """
    Main backend pipeline.

    Flow:
    User Question
        ↓
    Retrieve Relevant Chunks
        ↓
    Generate AI Answer
        ↓
    Return Answer + Sources
    """

    # Retrieve relevant chunks
    results = search(question)

    # Build context for Gemini
    context = "\n\n".join(chunk["text"] for chunk in results)

    # Generate answer
    answer = generate_answer(question, context)

    # Prepare source information
    sources = []

    for chunk in results:
        sources.append({
            "chapter": chunk["source"],
            "score": round(chunk.get("score", 0), 4)
        })

    # Remove duplicate chapters
    unique_sources = []
    seen = set()

    for source in sources:
        if source["chapter"] not in seen:
            seen.add(source["chapter"])
            unique_sources.append(source)

    return {
        "answer": answer,
        "sources": unique_sources
    }


def generate_quiz_from_question(question: str):

    results = search(question)

    context = "\n\n".join([r["text"] for r in results])

    quiz = generate_quiz(context)

    return {
        "quiz": quiz["quiz"],
        "sources": list(set([r["source"] for r in results]))
    }