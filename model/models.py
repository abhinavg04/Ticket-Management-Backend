from sqlmodel import SQLModel,Field,Relationship
from uuid import UUID,uuid4
from typing import Optional,List
from datetime import date
from enum import Enum
from sqlalchemy import Column, Date



class PriorityEnum(str, Enum):
    low = "Low"
    medium = "Medium"
    high = "High"


class StatusEnum(str, Enum):
    open = "Open"
    in_progress = "In Progress"
    closed = "Closed"
class Category(str,Enum):
    network = 'Network'
    wifi = 'Wifi'
    security = 'Security'
    software = 'Software'
    hardware = 'Hardware'

class Role(str, Enum):
    ADMIN = "admin"
    ENGINEER = "engineer"
    USER = "user"

class Ticket(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    ticket_id: Optional[str] = Field(
        default=None,
        index=True,
        unique=True
    )
    reported_by_id: UUID = Field(foreign_key="user.id")
    reported_by: "User" = Relationship(
        back_populates='reported_tickets',
        sa_relationship_kwargs={
            "foreign_keys": "Ticket.reported_by_id"
        }
    )
    date_reported: date = Field(
        sa_column=Column(
            Date,
            default=date.today 
        )
    )
    category:Category = Category.network
    issue_description: str
    assigned_to_id: Optional[UUID] = Field(
        default=None,
        foreign_key="user.id"
    )
    assigned_to: Optional["User"] = Relationship(
        back_populates='assigned_tickets',
        sa_relationship_kwargs={
            'foreign_keys':'Ticket.assigned_to_id'
        }
    )

    priority: PriorityEnum = PriorityEnum.medium
    status: StatusEnum = StatusEnum.open

    root_cause: Optional[str] = None
    resolution_summary: Optional[str] = None

    date_closed: Optional[date] = None

class User(SQLModel,table=True):
    id:UUID = Field(default_factory=uuid4,primary_key=True)
    username:str = Field(unique=True)
    password:str
    role:Role = Role.USER
    
    # Tickets ASSIGNED to this user
    assigned_tickets: List["Ticket"] = Relationship(
        back_populates="assigned_to",
        sa_relationship_kwargs={
            "foreign_keys": "Ticket.assigned_to_id"
        }
    )

    # Tickets REPORTED by this user
    reported_tickets: List["Ticket"] = Relationship(
        back_populates="reported_by",
        sa_relationship_kwargs={
            "foreign_keys": "Ticket.reported_by_id"
        }
    )