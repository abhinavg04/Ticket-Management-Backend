from uuid import UUID
from sqlmodel import Session, select
from core.db import get_session
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated, List
from fastapi import Depends,HTTPException,status,APIRouter
from core.config import settings
from datetime import timedelta
from model.models import User,UserStatus,Role
from pydantic import BaseModel
from core.auth import authenticate_user,create_access_token,get_current_user
from schema import UserCreate,UserPublic
from crud.crud_user import get_user_by_username,create_user


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)
class Token(BaseModel):
    access_token: str
    token_type: str
    
@router.put("/{user_id}/{status}")
async def updateStatus(
    user_id: UUID,  
    status:UserStatus,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != Role.ADMIN:
        raise HTTPException(status_code=403)

    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404)

    user.status = status
    session.add(user)
    session.commit()

    return {"message": f"User {status}"}
    
@router.get("/getAll",status_code=status.HTTP_200_OK,response_model=List[UserPublic])
async def getAllUser(session:Annotated[Session,Depends(get_session)],user_status :UserStatus|None = None):
    users = select(User).where(User.role != Role.ADMIN)
    if user_status:
        users = users.where(User.status == user_status.value)
    return session.exec(users).all()
    
    
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=UserPublic)
async def createUser(
    user_data:UserCreate,
    session:Annotated[Session,Depends(get_session)]
):
    user = get_user_by_username(user_data.username,session=session)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='A user with username already exists'
        )
    new_user = create_user(user_data,session=session)
    return new_user
    
@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session:Annotated[Session,Depends(get_session)]
) -> Token:
    user = authenticate_user(form_data.username, form_data.password,session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username,"role":user.role}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=UserPublic)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return current_user