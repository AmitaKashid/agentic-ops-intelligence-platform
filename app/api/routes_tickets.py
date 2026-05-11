from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.crud import get_all_tickets
from app.schemas import TicketResponse

router = APIRouter(prefix="/api/v1/tickets", tags=["Tickets"])


@router.get("", response_model=List[TicketResponse])
def list_tickets(db: Session = Depends(get_db)):
    return get_all_tickets(db)