import faiss
import numpy as np
import pickle

from app.config import VECTOR_STORE, FAISS_INDEX_PATH, CHUNKS_PATH

VECTOR_STORE.mkdir(exist_ok=True)


def save_index(embeddings: np.ndarray, chunks: list[dict]) -> None:
    """
    Save embeddings and metadata into the FAISS vector store.
    """

    embeddings = np.asarray(embeddings, dtype="float32")

    if embeddings.size == 0:
        raise ValueError("No embeddings available to create FAISS index.")

    faiss.normalize_L2(embeddings)

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)

    faiss.write_index(index, str(FAISS_INDEX_PATH))

    with open(CHUNKS_PATH, "wb") as f:
        pickle.dump(chunks, f)

    print(f"✅ Saved {len(chunks)} chunks to FAISS.")