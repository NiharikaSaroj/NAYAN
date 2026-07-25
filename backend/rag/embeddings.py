from sentence_transformers import SentenceTransformer

from app.config import EMBEDDING_MODEL

model = SentenceTransformer(EMBEDDING_MODEL)


def generate_embeddings(chunks):
    texts = [chunk["text"] for chunk in chunks]

    embeddings = model.encode(
        texts,
        show_progress_bar=True,
        convert_to_numpy=True
    )

    return embeddings