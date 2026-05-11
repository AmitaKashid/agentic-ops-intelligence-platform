from app.db.database import Base, SessionLocal, engine
from app.db.seed import seed_database
from app.tools.sql_tool import infer_region, infer_service, query_service_metrics


def setup_module():
    Base.metadata.create_all(bind=engine)
    seed_database()


def test_infer_payment_service():
    assert infer_service("payment failures in EU") == "payment-service"


def test_infer_auth_service():
    assert infer_service("login failures for enterprise users") == "auth-service"


def test_infer_region_eu():
    assert infer_region("EU customers are affected") == "EU"


def test_infer_region_us():
    assert infer_region("US customers are affected") == "US"


def test_query_payment_metrics_eu():
    db = SessionLocal()

    try:
        result = query_service_metrics(
            db=db,
            query="payment failures in EU",
        )

        assert result["tool_name"] == "sql_tool"
        assert result["service"] == "payment-service"
        assert result["region"] == "EU"
        assert result["records_found"] >= 1
        assert len(result["evidence"]) >= 1

        first_metric = result["raw_metrics"][0]
        assert first_metric["service"] == "payment-service"
        assert first_metric["region"] == "EU"

    finally:
        db.close()