from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import os
from pathlib import Path
from database import SessionLocal
from models import User

# Directory to store uploaded images
UPLOAD_DIR = "uploads"
Path(UPLOAD_DIR).mkdir(exist_ok=True)

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(
    prefix="/auth",
    tags=["Registration and Authentication of Users "]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/Register-User", status_code=201)
async def Register_User(
    db: db_dependency,
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    image: UploadFile = File(None),
):

    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email is already registered")


    image_url = None
    if image:
        try:
            file_path = os.path.join(UPLOAD_DIR, image.filename)
            with open(file_path, "wb") as f:
                f.write(await image.read())
            image_url = f"/{UPLOAD_DIR}/{image.filename}"
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error uploading image: {str(e)}")


    try:
        new_user = User(
            name=name,
            email=email,
            hashed_password=bcrypt_context.hash(password),
            profile_picture_url=image_url,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"message": "User registered successfully", "user_id": new_user.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating user: {str(e)}")
