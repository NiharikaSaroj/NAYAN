from pathlib import Path

# =====================================
# Project Paths
# =====================================

BASE_DIR = Path(__file__).resolve().parent.parent

KNOWLEDGE_BASE = BASE_DIR / "knowledge_base"

VECTOR_STORE = BASE_DIR / "vector_store"

FAISS_INDEX_PATH = VECTOR_STORE / "index.faiss"

CHUNKS_PATH = VECTOR_STORE / "metadata.pkl"

# =====================================
# AI Models
# =====================================

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

LLM_MODEL = "models/gemini-flash-latest"

# =====================================
# Retrieval Settings
# =====================================

TOP_K = 5