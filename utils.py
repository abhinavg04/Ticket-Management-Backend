from datetime import date
from sqlmodel import Session, select
from sqlalchemy import func
from model.models import Ticket

def generate_ticket_id(db: Session) -> str:
    today = date.today()
    date_str = today.strftime("%Y%m%d")

    # Count today's tickets
    count_stmt = select(func.count()).where(
        Ticket.date_reported == today
    )
    today_count = db.exec(count_stmt).one()

    sequence = today_count + 1

    return f"TKT-{date_str}-{sequence:04d}"