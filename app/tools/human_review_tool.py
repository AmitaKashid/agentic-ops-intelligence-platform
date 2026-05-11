from typing import Optional

from sqlalchemy.orm import Session

from app.db.crud import create_human_review_case
from app.utils.ids import generate_review_case_id


def should_send_to_human_review(
    confidence: float,
    rule_decision: str,
    evidence_count: int,
) -> bool:
    if rule_decision == "HUMAN_REVIEW":
        return True

    if confidence < 0.65:
        return True

    if evidence_count == 0:
        return True

    return False


def create_review_case_if_needed(
    db: Session,
    query: str,
    confidence: float,
    human_review_required: bool,
    reason: Optional[str] = None,
):
    if not human_review_required:
        return None

    case_reason = reason or "Low confidence or insufficient evidence."

    return create_human_review_case(
        db=db,
        case_id=generate_review_case_id(),
        query=query,
        reason=case_reason,
        confidence=confidence,
    )