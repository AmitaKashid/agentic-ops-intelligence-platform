import json
from typing import Any, Dict

from sqlalchemy.orm import Session

from app.db.crud import create_agent_trace


def write_trace(
    db: Session,
    trace_id: str,
    query: str,
    task_type: str,
    selected_tools: list[str],
    confidence: float,
    human_review_required: bool,
    final_decision: str,
    trace_payload: Dict[str, Any],
):
    trace_json = json.dumps(trace_payload, indent=2)

    return create_agent_trace(
        db=db,
        trace_id=trace_id,
        query=query,
        task_type=task_type,
        selected_tools=",".join(selected_tools),
        confidence=confidence,
        human_review_required=human_review_required,
        final_decision=final_decision,
        trace_json=trace_json,
    )