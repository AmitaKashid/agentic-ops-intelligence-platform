from pathlib import Path

from app.retrieval.build_index import main as build_index
from app.tools.rag_tool import retrieve_policy_evidence


def setup_module():
    index_path = Path("app/data/vector_index/faiss.index")
    metadata_path = Path("app/data/vector_index/chunks.json")

    if not index_path.exists() or not metadata_path.exists():
        build_index()


def test_rag_tool_retrieves_policy_evidence():
    result = retrieve_policy_evidence(
        query="What does the SLA policy say about payment failure escalation?",
        top_k=3,
    )

    assert result["tool_name"] == "rag_tool"
    assert result["records_found"] > 0
    assert len(result["evidence"]) > 0

    first_item = result["evidence"][0]

    assert first_item["source"] == "rag_tool"
    assert "Retrieved from" in first_item["content"]
    assert "citation" in first_item
    assert "score" in first_item