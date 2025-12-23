from pydantic import BaseModel,Field
from typing import Optional
from uuid import UUID
from model.models import Category, PriorityEnum,StatusEnum,UserStatus,Role
from datetime import date


class UserCreate(BaseModel):
    username:str
    password:str
    email:str
    emp_id:str
    full_name:str

    
class UserPublic(BaseModel):
    id:UUID
    username:str
    role:str
    email:str
    emp_id:str
    full_name:str
    status:UserStatus
    
class TicketCreate(BaseModel):
    category: Category
    issue_description: str
    priority: PriorityEnum = PriorityEnum.medium
    assigned_to_id:UUID

class TicketUpdate(BaseModel):
    assigned_to_id: Optional[UUID] = None
    status: Optional[StatusEnum] = None
    priority: Optional[PriorityEnum] = None
    root_cause: Optional[str] = None
    resolution_summary: Optional[str] = None
    
class TicketPublic(BaseModel):
    id: int
    ticket_id: str
    category: Category
    issue_description: str
    priority: PriorityEnum
    status: StatusEnum

    reported_by: str          # username
    assigned_to: Optional[str]

    date_reported: date
    date_closed: Optional[date]

    root_cause: Optional[str]
    resolution_summary: Optional[str]

class TicketUpdate(BaseModel):
    status: StatusEnum
    root_cause: Optional[str]
    resolution_summary: Optional[str]