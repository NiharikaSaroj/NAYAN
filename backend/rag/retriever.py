import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from rag.llm import generate_answer

model = SentenceTransformer("all-MiniLM-L6-v2")

index = faiss.read_index("vector_store/index.faiss")

with open("vector_store/metadata.pkl", "rb") as f:
    metadata = pickle.load(f)


def search(query, k=5):
    query_embedding = model.encode([query], convert_to_numpy=True).astype("float32")

    faiss.normalize_L2(query_embedding)

    distances, indices = index.search(query_embedding, k)

    results = []

    for idx in indices[0]:
        results.append(metadata[idx])

    return results


if __name__ == "__main__":
    query = input("Ask: ")

    results = search(query)

    context = "\n\n".join([r["text"] for r in results])

    answer = generate_answer(query, context)

    print("\n========== NAYAN ==========\n")
    print(answer)