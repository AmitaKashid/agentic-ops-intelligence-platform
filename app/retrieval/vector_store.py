import json
from pathlib import Path
from typing import Dict, List, Tuple

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


VECTOR_DIR = Path("app/data/vector_index")
INDEX_PATH = VECTOR_DIR / "faiss.index"
METADATA_PATH = VECTOR_DIR / "chunks.json"
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


_model = None


def get_embedding_model() -> SentenceTransformer:
    global _model

    if _model is None:
        _model = SentenceTransformer(EMBEDDING_MODEL_NAME)

    return _model


def embed_texts(texts: List[str]) -> np.ndarray:
    model = get_embedding_model()

    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True,
    )

    return embeddings.astype("float32")


def save_vector_index(chunks: List[Dict[str, str]]) -> None:
    VECTOR_DIR.mkdir(parents=True, exist_ok=True)

    texts = [chunk["text"] for chunk in chunks]
    embeddings = embed_texts(texts)

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)

    faiss.write_index(index, str(INDEX_PATH))

    METADATA_PATH.write_text(
        json.dumps(chunks, indent=2),
        encoding="utf-8",
    )


def load_vector_index() -> Tuple[faiss.Index, List[Dict[str, str]]]:
    if not INDEX_PATH.exists() or not METADATA_PATH.exists():
        raise FileNotFoundError(
            "Vector index not found. Run: python -m app.retrieval.build_index"
        )

    index = faiss.read_index(str(INDEX_PATH))

    chunks = json.loads(
        METADATA_PATH.read_text(encoding="utf-8")
    )

    return index, chunks


def search_vector_index(
    query: str,
    top_k: int = 3,
) -> List[Dict[str, object]]:
    index, chunks = load_vector_index()

    query_embedding = embed_texts([query])

    scores, indices = index.search(query_embedding, top_k)

    results = []

    for score, index_id in zip(scores[0], indices[0]):
        if index_id == -1:
            continue

        chunk = chunks[index_id]

        results.append(
            {
                "chunk_id": chunk["chunk_id"],
                "source": chunk["source"],
                "text": chunk["text"],
                "score": float(score),
            }
        )

    return results