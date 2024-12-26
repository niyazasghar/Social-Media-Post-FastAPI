from datetime import timedelta, datetime, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from starlette import status

from database import SessionLocal
from models import User

router = APIRouter()
router = APIRouter(
    prefix='/auth',
    tags=['APIs of Authentication of Users']
)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
db_dependency = Annotated[Session, Depends(get_db)]
SECRET_KEY = '197b2c37c391bed93fe80344fe73b806947a65e36206e05a1a23c2fa12702fe3'
ALGORITHM = 'HS256'

db_dependency = Annotated[Session, Depends(get_db)]
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
formData_dependency = Annotated[OAuth2PasswordRequestForm, Depends()]
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')




def authenticateUser(username, password, db):
    user= db.query(User).filter(username == User.name).first()
    if not user or not bcrypt_context.verify(password, user.hashed_password):
       False
    else:
        return user


def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)




@router.post("/token")
def login_for_access_token(db: db_dependency, formData: formData_dependency):
    user= authenticateUser(formData.username, formData.password,db)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    else:
        token = create_access_token(user.name, user.id, timedelta(minutes=20))
        return {'access_token': token, 'token_type': 'bearer'}


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        name: str = payload.get('sub')
        id: int = payload.get('id')
        if name is None or id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user.')
        return {'name': name, 'id': id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')


