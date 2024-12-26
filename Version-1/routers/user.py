from typing import Annotated, List

from fastapi import APIRouter, Depends
from database import SessionLocal
from schemas import UserCreateRequest, UserResponse
from sqlalchemy.orm import Session
from models import User

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(
    prefix='/user',
    tags=['APIs of Users Registration']
)

@router.post('/Register-User', status_code=201)
def Register_User(db: db_dependency, usercCreateRequest: UserCreateRequest):
    new_user = User(
        name=usercCreateRequest.name,
        email=usercCreateRequest.email,
        profile_picture_url=usercCreateRequest.profile_picture_url,
        password=usercCreateRequest.password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully"}

@router.get('/fetch-users', status_code=200, response_model=List[UserResponse])
def View_User(db: db_dependency):
    users = db.query(User).all()
    return users
