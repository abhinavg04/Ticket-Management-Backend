from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from model.models import Ticket
from core.db import get_session
from utils import generate_ticket_id

router = APIRouter(prefix="/tickets", tags=["Tickets"])

@router.post("/", response_model=Ticket)
def create_ticket(ticket: Ticket, session: Session = Depends(get_session)):
    ticket.ticket_id = generate_ticket_id(session)
    session.add(ticket)
    session.commit()
    session.refresh(ticket)
    return ticket

@router.get("/", response_model=List[Ticket])
def get_tickets(session: Session = Depends(get_session)):
    return session.exec(select(Ticket)).all()

@router.get("/{ticket_id}", response_model=Ticket)
def get_ticket(ticket_id: int, session: Session = Depends(get_session)):
    ticket = session.get(Ticket, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket

@router.put("/{ticket_id}", response_model=Ticket)
def update_ticket(ticket_id: int, updated_ticket: Ticket, session: Session = Depends(get_session)):
    ticket = session.get(Ticket, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    ticket_data = updated_ticket.dict(exclude_unset=True)
    for key, value in ticket_data.items():
        setattr(ticket, key, value)

    session.add(ticket)
    session.commit()
    session.refresh(ticket)
    return ticket

@router.delete("/{ticket_id}")
def delete_ticket(ticket_id: int, session: Session = Depends(get_session)):
    ticket = session.get(Ticket, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    session.delete(ticket)
    session.commit()
    return {"message": "Ticket deleted successfully"}
