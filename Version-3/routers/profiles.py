import os
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from Schemas_v3 import UserProfileResponse, PostSummary
from models import User, Post
from database import SessionLocal
from routers.auth import get_db, get_current_user

router = APIRouter(
    prefix="/profiles",
    tags=["APIs related to profiles of Users"]
)

# Directory for uploaded files
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

### Fetch User Profile
@router.get("/profile", response_model=UserProfileResponse)
def get_user_profile(db: db_dependency, user: user_dependency):
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")

    # Fetch user details
    user_details = db.query(User).filter(User.id == user["id"]).first()
    if not user_details:
        raise HTTPException(status_code=404, detail="User not found")

    # Fetch user's posts
    posts = db.query(Post).filter(Post.user_id == user["id"]).all()

    # Return user profile response
    return UserProfileResponse(
        id=user_details.id,
        name=user_details.name,
        email=user_details.email,
        profile_picture_url=user_details.profile_picture_url,
        follower_count=user_details.followers_count,
        following_count=user_details.following_count,
        posts=[PostSummary(
            id=post.id,
            text=post.text,
            image_url=post.image_url
        ) for post in posts]
    )

### Update User Profile
@router.put("/profile/update", response_model=UserProfileResponse)
async def update_user_profile(
    name: str,
    profile_picture: UploadFile = File(None),
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")

    # Fetch user details
    user_details = db.query(User).filter(User.id == user["id"]).first()
    if not user_details:
        raise HTTPException(status_code=404, detail="User not found")

    # Update user details
    user_details.name = name

    # Handle profile picture upload
    if profile_picture:
        file_path = os.path.join(UPLOAD_DIR, profile_picture.filename)
        with open(file_path, "wb") as f:
            f.write(await profile_picture.read())
        user_details.profile_picture_url = f"/{file_path}"

    db.commit()
    db.refresh(user_details)

    # Return updated user profile response
    return UserProfileResponse(
        id=user_details.id,
        name=user_details.name,
        email=user_details.email,
        profile_picture_url=user_details.profile_picture_url,
        follower_count=user_details.followers_count,
        following_count=user_details.following_count,
        posts=[]
    )
