from pydantic import BaseModel
from uuid import UUID

class UserCreate(BaseModel):
    username:str
    password:str
    
class UserPublic(BaseModel):
    id:UUID
    username:str
    role:str