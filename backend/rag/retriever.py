import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

from app.config import (
    EMBEDDING_MODEL,
    FAISS_INDEX_PATH,
    CHUNKS_PATH,
    TOP_K,
)
from rag.llm import generate_answer

model = SentenceTransformer(EMBEDDING_MODEL)

index = faiss.read_index(str(FAISS_INDEX_PATH))

with open(CHUNKS_PATH, "rb") as f:
    metadata = pickle.load(f)


def search(query, k=TOP_K):
    query_embedding = model.encode([query], convert_to_numpy=True).astype("float32")

    faiss.normalize_L2(query_embedding)

    distances, indices = index.search(query_embedding, k)

    results = []

    for score, idx in zip(distances[0], indices[0]):

        if idx == -1:
            continue

        chunk = metadata[idx].copy()

        chunk["score"] = float(score)

        results.append(chunk)

    return results

if __name__ == "__main__":
    query = input("Ask: ")

    results = search(query)

    context = "\n\n".join([r["text"] for r in results])

    answer = generate_answer(query, context)

    print("\n========== NAYAN ==========\n")
    print(answer)