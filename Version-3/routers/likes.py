
from typing import Annotated

from fastapi import APIRouter, Depends , HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Post, Like
from routers.auth import get_current_user
from schemas import PostResponse

router = APIRouter(
    prefix="/likes",
    tags=["APIs related to likes on the Posts"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
@router.post("/like/{post_id}")
def like_post(post_id: int, user: user_dependency, db: db_dependency):
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")

    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    like = db.query(Like).filter(Like.post_id == post_id, Like.user_id == user["id"]).first()
    if like:
        raise HTTPException(status_code=400, detail="You have already liked this post")

    # Add a new like
    new_like = Like(post_id=post_id, user_id=user["id"])
    db.add(new_like)

    # Increment like count
    post.like_count += 1
    db.commit()

    return {"message": "Post liked successfully", "like_count": post.like_count}

@router.delete("/unlike/{post_id}")
def unlike_post(post_id: int, user: user_dependency, db: db_dependency):
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")

    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    like = db.query(Like).filter(Like.post_id == post_id, Like.user_id == user["id"]).first()
    if not like:
        raise HTTPException(status_code=404, detail="You have not liked this post")

    db.delete(like)
    post.like_count -= 1
    db.commit()

    return {"message": "Post unliked successfully", "like_count": post.like_count}
