from sqlmodel import select, func
from datetime import datetime
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from model.models import Ticket,StatusEnum,PriorityEnum
from core.db import get_session
from pydantic import BaseModel

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])
class DashboardStats(BaseModel):
    total_tickets: int
    open_tickets: int
    in_progress_tickets: int
    closed_tickets: int
    critical_tickets: int

@router.get("/stats", response_model=DashboardStats)
def get_dashboard_stats(
    session: Session = Depends(get_session),
):
    total_tickets = session.exec(
        select(func.count(Ticket.id))
    ).one()

    open_tickets = session.exec(
        select(func.count(Ticket.id)).where(Ticket.status == StatusEnum.open)
    ).one()

    in_progress_tickets = session.exec(
        select(func.count(Ticket.id)).where(Ticket.status == StatusEnum.in_progress)
    ).one()

    closed_tickets = session.exec(
        select(func.count(Ticket.id)).where(Ticket.status == StatusEnum.closed)
    ).one()

    critical_tickets = session.exec(
        select(func.count(Ticket.id)).where(Ticket.priority == PriorityEnum.high)
    ).one()

    # Avg resolution time (only closed tickets)
    # avg_resolution = session.exec(
    #     select(
    #         func.avg(
    #             func.timestampdiff(
    #                 text("HOUR"),
    #                 Ticket.date_reported,
    #                 Ticket.date_closed
    #             )
    #         )
    #     ).where(Ticket.closed_at.is_not(None))
    # ).one()

    return {
        "total_tickets": total_tickets,
        "open_tickets": open_tickets,
        "in_progress_tickets": in_progress_tickets,
        "closed_tickets": closed_tickets,
        "critical_tickets": critical_tickets,
    }
