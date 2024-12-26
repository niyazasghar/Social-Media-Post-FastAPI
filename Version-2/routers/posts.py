from datetime import datetime
from typing import Annotated, List
import os
from pathlib import Path
from venv import logger

from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Post, User
from routers.auth import get_current_user
from schemas import  PostResponse

router = APIRouter(
    prefix='/post',
    tags=['APIs of Posts of Social Media']
)

# Directory to store uploaded images
UPLOAD_DIR = "uploads"
Path(UPLOAD_DIR).mkdir(exist_ok=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
@router.get('/read-user-posts/{user_id}', response_model=List[PostResponse])
def read_all_posts_of_user(user_id: int, user: user_dependency , db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    return db.query(Post).filter(Post.user_id == user_id).all()


@router.get('/read-post/{id}', response_model=PostResponse)
def get_post_by_id(id: int, user: user_dependency,db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    post = db.query(Post).filter(Post.id == id , user.get('id') == Post.user_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


from sqlalchemy.orm import joinedload

@router.post('/create-posts', status_code=201, response_model=PostResponse)
async def create_post(
    user: user_dependency,
    db: db_dependency,
    text: str = Form(...),
    image: UploadFile = File(None)

):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    # Create post
    image_url = None
    if image:
        file_path = os.path.join(UPLOAD_DIR, image.filename)
        with open(file_path, "wb") as f:
            f.write(await image.read())
        image_url = f"/{UPLOAD_DIR}/{image.filename}"

    # Check if user exists
    owner = db.query(User).filter(User.id == user.get('id')).first()
    if not owner:
        raise HTTPException(status_code=404, detail="User not found")

    new_post = Post(
        text=text,
        image_url=image_url,
        user_id=user.get('id'),
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    # Eagerly load the owner relationship
    post_with_owner = db.query(Post).options(joinedload(Post.owner)).filter(Post.id == new_post.id).first()
    return post_with_owner
@router.put('/update-post', status_code=200, response_model=PostResponse)
async def update_post(
    user: user_dependency,
    db: db_dependency,
    id: int = Form(...),
    text: str = Form(...),
    image: UploadFile = File(None)
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    try:
        # Fetch the post and ensure it belongs to the authenticated user
        existing_post = db.query(Post).filter(
            Post.id == id, Post.user_id == user.get('id')
        ).options(joinedload(Post.owner)).first()

        if not existing_post:
            raise HTTPException(status_code=404, detail="Post not found or not authorized to edit")

        # Update text
        existing_post.text = text

        # Handle file upload if provided
        if image:
            # Delete old image
            if existing_post.image_url:
                old_file_path = os.path.join(UPLOAD_DIR, os.path.basename(existing_post.image_url))
                if os.path.exists(old_file_path):
                    os.remove(old_file_path)

            # Save new image
            file_path = os.path.join(UPLOAD_DIR, image.filename)
            with open(file_path, "wb") as f:
                f.write(await image.read())
            existing_post.image_url = f"/{UPLOAD_DIR}/{image.filename}"

        # Update timestamp
        existing_post.updated_at = datetime.now()

        # Commit changes
        db.commit()
        db.refresh(existing_post)

        return existing_post
    except HTTPException as http_exc:
        raise http_exc  # Re-raise HTTPException
    except Exception as e:
        logger.error(f"Error updating post: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.delete('/delete-post/{id}', status_code=200)
def delete_post(user: user_dependency,db: db_dependency, id: int):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    # Fetch the post and ensure it belongs to the authenticated user
    post = db.query(Post).filter(
        Post.id == id, Post.user_id == user.get('id')
    ).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found or not authorized to delete")

    # Delete the post
    db.delete(post)
    db.commit()

    return {"detail": f"Post with id {id} deleted successfully"}
