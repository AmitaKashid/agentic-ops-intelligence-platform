from sqlalchemy.orm import Session

from app.db.models import (
    AgentTrace,
    HumanReviewCase,
    Incident,
    OperationalLog,
    ServiceMetric,
    Ticket,
)


def get_all_tickets(db: Session):
    return db.query(Ticket).all()


def get_ticket_by_id(db: Session, ticket_id: str):
    return db.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()


def get_metrics_by_service_region(db: Session, service: str, region: str):
    return (
        db.query(ServiceMetric)
        .filter(ServiceMetric.service == service)
        .filter(ServiceMetric.region == region)
        .all()
    )


def get_logs_by_service_region(db: Session, service: str, region: str):
    return (
        db.query(OperationalLog)
        .filter(OperationalLog.service == service)
        .filter(OperationalLog.region == region)
        .all()
    )


def get_incidents_by_service_region(db: Session, service: str, region: str):
    return (
        db.query(Incident)
        .filter(Incident.service == service)
        .filter(Incident.region == region)
        .all()
    )


def create_human_review_case(
    db: Session,
    case_id: str,
    query: str,
    reason: str,
    confidence: float,
):
    case = HumanReviewCase(
        case_id=case_id,
        query=query,
        reason=reason,
        confidence=confidence,
        status="pending",
    )
    db.add(case)
    db.commit()
    db.refresh(case)
    return case


def get_human_review_cases(db: Session):
    return db.query(HumanReviewCase).all()


def resolve_human_review_case(db: Session, case_id: str):
    case = db.query(HumanReviewCase).filter(HumanReviewCase.case_id == case_id).first()
    if not case:
        return None

    case.status = "resolved"
    db.commit()
    db.refresh(case)
    return case


def create_agent_trace(
    db: Session,
    trace_id: str,
    query: str,
    task_type: str,
    selected_tools: str,
    confidence: float,
    human_review_required: bool,
    final_decision: str,
    trace_json: str,
):
    trace = AgentTrace(
        trace_id=trace_id,
        query=query,
        task_type=task_type,
        selected_tools=selected_tools,
        confidence=confidence,
        human_review_required=human_review_required,
        final_decision=final_decision,
        trace_json=trace_json,
    )
    db.add(trace)
    db.commit()
    db.refresh(trace)
    return trace


def get_all_traces(db: Session):
    return db.query(AgentTrace).order_by(AgentTrace.created_at.desc()).all()


def get_trace_by_id(db: Session, trace_id: str):
    return db.query(AgentTrace).filter(AgentTrace.trace_id == trace_id).first()