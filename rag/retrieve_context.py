"""
retrieve_context.py

Vector-based RAG retrieval using:
- SentenceTransformers
- FAISS
- Pre-built index + documents

Used for career guidance, cognitive insights, accessibility hints.
"""

import os
import pickle
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import streamlit as st

# --------------------------------------------------
# CONFIG
# --------------------------------------------------
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
INDEX_DIR = os.path.join(PROJECT_ROOT, "src", "rag", "index")

INDEX_PATH = os.path.join(INDEX_DIR, "faiss.index")
DOCS_PATH = os.path.join(INDEX_DIR, "docs.pkl")

# --------------------------------------------------
# LOAD EMBEDDING MODEL (CPU SAFE)
# --------------------------------------------------
_embedder = SentenceTransformer(MODEL_NAME, device="cpu")


def embed_texts(texts):
    """
    Generate normalized embeddings
    """
    return _embedder.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

INDEX_PATH = "src/rag/index/faiss.index"
DOCS_PATH = "src/rag/index/docs.pkl"

@st.cache_resource(show_spinner=False)
def load_faiss_index():
    index = faiss.read_index(INDEX_PATH)

    with open(DOCS_PATH, "rb") as f:
        documents = pickle.load(f)

    return index, documents



def retrieve_context(query: str, k: int = 3) -> str:
    """
    Retrieve top-k relevant knowledge snippets
    using vector similarity search.
    """

    # Safety check
    if not os.path.exists(INDEX_PATH) or not os.path.exists(DOCS_PATH):
        return ""

    # Load FAISS index
    index = faiss.read_index(INDEX_PATH)

    # Load documents
    with open(DOCS_PATH, "rb") as f:
        documents = pickle.load(f)

    if not documents:
        return ""

    # Embed query
    query_vec = embed_texts([query])

    # Search
    distances, indices = index.search(query_vec, k)

    results = []
    for idx in indices[0]:
        if 0 <= idx < len(documents):
            results.append(documents[idx])

    return "\n\n".join(results)


# --------------------------------------------------
# LOCAL TEST (OPTIONAL)
# --------------------------------------------------
if __name__ == "__main__":
    test_query = "career guidance for strong memory and attention"
    print(retrieve_context(test_query))
