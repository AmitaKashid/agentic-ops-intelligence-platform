from fastapi import FastAPI

from app.config import settings
from app.api.routes_analysis import router as analysis_router
from app.api.routes_tickets import router as tickets_router
from app.api.routes_review import router as review_router
from app.api.routes_traces import router as traces_router
from app.api.routes_evaluation import router as evaluation_router
from app.schemas import HealthResponse


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "Enterprise-style agentic AI backend for operational ticket triage, "
        "tool routing, evidence-grounded recommendations, and human review."
    ),
)

app.include_router(analysis_router)
app.include_router(tickets_router)
app.include_router(review_router)
app.include_router(traces_router)
app.include_router(evaluation_router)


@app.get("/health", response_model=HealthResponse, tags=["System"])
def health_check():
    return HealthResponse(
        status="ok",
        app_name=settings.app_name,
        version=settings.app_version,
    )