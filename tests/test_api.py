from fastapi.testclient import TestClient

from app.db.database import Base, engine
from app.db.seed import seed_database
from app.main import app
from app.retrieval.build_index import main as build_index


client = TestClient(app)


def setup_module():
    Base.metadata.create_all(bind=engine)
    seed_database()
    build_index()


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "ok"
    assert "Agentic Operations Intelligence Platform" in data["app_name"]


def test_list_tickets_endpoint():
    response = client.get("/api/v1/tickets")

    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert len(data) >= 1
    assert "ticket_id" in data[0]


def test_analyze_ticket_payment_escalation():
    payload = {
        "query": "EU customers are reporting payment failures after checkout. Should this be escalated?",
        "ticket_id": "TCK-1001",
    }

    response = client.post("/api/v1/analyze-ticket", json=payload)

    assert response.status_code == 200
    data = response.json()

    assert data["ticket_id"] == "TCK-1001"
    assert data["task_type"] == "escalation_decision"
    assert data["priority"] == "P1"
    assert data["human_review_required"] is False
    assert "sql_tool" in data["tools_used"]
    assert "log_search_tool" in data["tools_used"]
    assert "rag_tool" in data["tools_used"]
    assert "rule_validator" in data["tools_used"]
    assert len(data["evidence"]) >= 1
    assert data["trace_id"].startswith("trace_")


def test_analyze_ambiguous_ticket_goes_to_human_review():
    payload = {
        "query": "Something seems wrong with the application.",
        "ticket_id": "TCK-9999",
    }

    response = client.post("/api/v1/analyze-ticket", json=payload)

    assert response.status_code == 200
    data = response.json()

    assert data["task_type"] == "ambiguous"
    assert data["human_review_required"] is True
    assert data["trace_id"].startswith("trace_")


def test_traces_endpoint_after_analysis():
    response = client.get("/api/v1/traces")

    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)