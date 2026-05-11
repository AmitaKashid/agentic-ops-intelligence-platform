from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.agent.graph import run_agent_workflow
from app.db.database import get_db
from app.schemas import AnalyzeTicketRequest, AnalyzeTicketResponse

router = APIRouter(prefix="/api/v1", tags=["Analysis"])


@router.post("/analyze-ticket", response_model=AnalyzeTicketResponse)
def analyze_ticket(
    request: AnalyzeTicketRequest,
    db: Session = Depends(get_db),
):
    final_state = run_agent_workflow(
        db=db,
        query=request.query,
        ticket_id=request.ticket_id,
    )

    rule_result = final_state.get("rule_result")

    priority = None
    matched_rules = []

    if rule_result:
        priority = rule_result.get("priority")
        matched_rules = rule_result.get("matched_rules", [])

    return AnalyzeTicketResponse(
        ticket_id=request.ticket_id,
        task_type=final_state["task_type"],
        priority=priority,
        recommendation=final_state["recommendation"],
        confidence=final_state["confidence"],
        human_review_required=final_state["human_review_required"],
        tools_used=final_state.get("selected_tools", []),
        evidence=final_state.get("evidence", []),
        matched_rules=matched_rules,
        trace_id=final_state["trace_id"],
    )