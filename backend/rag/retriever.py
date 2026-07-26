import faiss
import pickle
from sentence_transformers import SentenceTransformer

from app.config import (
    EMBEDDING_MODEL,
    FAISS_INDEX_PATH,
    CHUNKS_PATH,
    TOP_K,
    SIMILARITY_THRESHOLD,
)

from rag.llm import generate_answer

model = SentenceTransformer(EMBEDDING_MODEL)

try:
    index = faiss.read_index(str(FAISS_INDEX_PATH))

    with open(CHUNKS_PATH, "rb") as f:
        metadata = pickle.load(f)

except Exception as e:
    raise RuntimeError(f"Failed to load vector store: {e}")


def search(query: str, k: int = TOP_K) -> list[dict]:
    """
    Retrieve the top-k most relevant chunks from the FAISS vector store.
    """

    if not query.strip():
        return []

    query_embedding = model.encode(
        [query],
        convert_to_numpy=True
    ).astype("float32")

    faiss.normalize_L2(query_embedding)

    distances, indices = index.search(query_embedding, k)

    results = []

    for score, idx in zip(distances[0], indices[0]):

        if idx == -1:
            continue

        # Ignore weak matches
        if float(score) < SIMILARITY_THRESHOLD:
            continue

        chunk = metadata[idx].copy()
        chunk["score"] = float(score)

        results.append(chunk)

    print(f"Retrieved {len(results)} relevant chunks.")
    return results


if __name__ == "__main__":
    query = input("Ask: ")

    results = search(query)

    print("\n===== Retrieved Chunks =====")

    for i, r in enumerate(results, 1):
        print(f"\nChunk {i}")
        print("Source:", r["source"])
        print("Score:", r["score"])
        print(r["text"][:500])
        
    context = "\n\n".join([r["text"] for r in results])

    answer = generate_answer(query, context)

    print("\n========== NAYAN ==========\n")
    print(answer)