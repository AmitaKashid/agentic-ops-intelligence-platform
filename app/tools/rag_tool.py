from typing import Any, Dict, List

from app.retrieval.retriever import retrieve_relevant_documents


def retrieve_policy_evidence(
    query: str,
    top_k: int = 3,
) -> Dict[str, Any]:
    retrieved_docs = retrieve_relevant_documents(
        query=query,
        top_k=top_k,
    )

    evidence = []

    for doc in retrieved_docs:
        score = float(doc["score"])

        if score >= 0.45:
            strength = "strong"
        elif score >= 0.30:
            strength = "moderate"
        else:
            strength = "weak"

        evidence.append(
            {
                "source": "rag_tool",
                "content": (
                    f"Retrieved from {doc['source']}: {doc['text']}"
                ),
                "strength": strength,
                "citation": doc["source"],
                "chunk_id": doc["chunk_id"],
                "score": score,
                "raw": doc,
            }
        )

    return {
        "tool_name": "rag_tool",
        "records_found": len(retrieved_docs),
        "evidence": evidence,
        "retrieved_documents": retrieved_docs,
    }