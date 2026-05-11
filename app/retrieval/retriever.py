from typing import Dict, List

from app.retrieval.vector_store import search_vector_index


def retrieve_relevant_documents(
    query: str,
    top_k: int = 3,
) -> List[Dict[str, object]]:
    return search_vector_index(query=query, top_k=top_k)