from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class AnalyzeTicketRequest(BaseModel):
    query: str = Field(..., min_length=5)
    ticket_id: Optional[str] = None


class EvidenceItem(BaseModel):
    source: str
    content: str
    strength: str


class AnalyzeTicketResponse(BaseModel):
    ticket_id: Optional[str]
    task_type: str
    priority: Optional[str]
    recommendation: str
    confidence: float
    human_review_required: bool
    tools_used: List[str]
    evidence: List[EvidenceItem]
    matched_rules: List[str]
    trace_id: str


class TicketResponse(BaseModel):
    ticket_id: str
    timestamp: str
    customer_tier: str
    service: str
    region: str
    description: str
    status: str

    class Config:
        from_attributes = True


class HumanReviewResponse(BaseModel):
    case_id: str
    query: str
    reason: str
    confidence: float
    status: str

    class Config:
        from_attributes = True


class TraceResponse(BaseModel):
    trace_id: str
    query: str
    task_type: str
    selected_tools: str
    confidence: float
    human_review_required: bool
    final_decision: str
    trace_json: str

    class Config:
        from_attributes = True


class HealthResponse(BaseModel):
    status: str
    app_name: str
    version: str