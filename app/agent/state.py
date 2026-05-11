from typing import Any, Dict, List, Optional, TypedDict

from app.schemas import EvidenceItem


class AgentState(TypedDict, total=False):
    # Request data
    query: str
    ticket_id: Optional[str]
    trace_id: str

    # Classification and planning
    task_type: str
    selected_tools: List[str]
    planner_reasons: List[str]

    # Tool outputs
    tool_outputs: Dict[str, Any]
    evidence: List[EvidenceItem]
    rule_result: Optional[Dict[str, Any]]

    # Evidence and confidence
    evidence_quality: Dict[str, Any]
    confidence: float

    # Review and response
    human_review_required: bool
    human_review_case_id: Optional[str]
    recommendation: str

    # Database session passed through runtime
    db: Any