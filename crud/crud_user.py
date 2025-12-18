from sqlmodel import Session,select
from model.models import User
from schema import UserCreate,UserPublic
from core.security import get_password_hash

def get_user_by_username(username: str,session:Session)->User:
    stm = select(User).where(User.username==username)
    res = session.exec(stm)
    return res.one_or_none()


def create_user(user_data:UserCreate,session:Session):
    user = User(
        username=user_data.username,
        password = get_password_hash(user_data.password)
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

