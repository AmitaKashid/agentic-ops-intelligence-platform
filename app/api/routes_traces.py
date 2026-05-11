from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.crud import get_all_traces, get_trace_by_id
from app.schemas import TraceResponse

router = APIRouter(prefix="/api/v1/traces", tags=["Traces"])


@router.get("", response_model=List[TraceResponse])
def list_traces(db: Session = Depends(get_db)):
    return get_all_traces(db)


@router.get("/{trace_id}", response_model=TraceResponse)
def read_trace(trace_id: str, db: Session = Depends(get_db)):
    trace = get_trace_by_id(db, trace_id)
    if not trace:
        raise HTTPException(status_code=404, detail="Trace not found")
    return trace