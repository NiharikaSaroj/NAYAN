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
# Retrieval
# =====================================

TOP_K = 5

# =====================================
# Chunking
# =====================================

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

# =====================================
# API
# =====================================

MAX_QUESTION_LENGTH = 500

# =====================================
# Logging
# =====================================

LOG_LEVEL = "INFO"
# =====================================
# Retrieval Settings
# =====================================

TOP_K = 5

# Minimum similarity score required
SIMILARITY_THRESHOLD = 0.45