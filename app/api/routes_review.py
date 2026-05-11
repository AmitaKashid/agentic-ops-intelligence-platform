from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.crud import get_human_review_cases, resolve_human_review_case
from app.schemas import HumanReviewResponse

router = APIRouter(prefix="/api/v1/human-review", tags=["Human Review"])


@router.get("", response_model=List[HumanReviewResponse])
def list_human_review_cases(db: Session = Depends(get_db)):
    return get_human_review_cases(db)


@router.post("/{case_id}/resolve", response_model=HumanReviewResponse)
def resolve_case(case_id: str, db: Session = Depends(get_db)):
    case = resolve_human_review_case(db, case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Human review case not found")
    return case