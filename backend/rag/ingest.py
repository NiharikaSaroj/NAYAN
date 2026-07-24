from pathlib import Path
import fitz

from cleaner import clean_text
from chunker import chunk_text

from embeddings import generate_embeddings

from vector_store import save_index

KNOWLEDGE_BASE = Path("knowledge_base")

# -----------------------------
# Load all PDFs
# -----------------------------
documents = []

pdf_files = list(KNOWLEDGE_BASE.rglob("*.pdf"))

print(f"Found {len(pdf_files)} PDF files.\n")

for pdf_path in pdf_files:
    document = fitz.open(pdf_path)

    full_text = ""

    for page in document:
        full_text += page.get_text()

    documents.append({
        "filename": pdf_path.name,
        "path": str(pdf_path),
        "text": clean_text(full_text)
    })

print(f"Loaded {len(documents)} documents.")

# -----------------------------
# Create Chunks
# -----------------------------
all_chunks = []

for doc in documents:
    chunks = chunk_text(doc["text"])

    for i, chunk in enumerate(chunks):
        all_chunks.append({
            "source": doc["filename"],
            "chunk_id": f"{doc['filename']}_{i}",
            "text": chunk
        })

print(f"Total Chunks: {len(all_chunks)}")

embeddings = generate_embeddings(all_chunks)

print(f"Embeddings Shape: {embeddings.shape}")

save_index(embeddings, all_chunks)

if all_chunks:
    print("\nFirst Chunk:\n")
    print(all_chunks[0]["text"][:500])
else:
    print("No chunks were created.")