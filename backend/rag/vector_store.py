import faiss
import numpy as np
import pickle
from pathlib import Path

VECTOR_STORE = Path("vector_store")
VECTOR_STORE.mkdir(exist_ok=True)

def save_index(embeddings, chunks):
    embeddings = np.array(embeddings).astype("float32")

    # Normalize embeddings for cosine similarity
    faiss.normalize_L2(embeddings)

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)

    faiss.write_index(index, str(VECTOR_STORE / "index.faiss"))

    with open(VECTOR_STORE / "metadata.pkl", "wb") as f:
        pickle.dump(chunks, f)

    print("✅ FAISS index saved.")