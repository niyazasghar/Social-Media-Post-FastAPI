
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from Schemas_v2 import CommentCreateRequest, CommentsResponse
from database import SessionLocal
from models import Comment, Post, User
from routers.auth import get_current_user

router = APIRouter(
    prefix="/comments",
    tags=["APIs related to Comments on the Post"]
)

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.post("/add_comment", status_code=201, response_model=CommentsResponse)
def add_comment(
    user: user_dependency,
    db: db_dependency,
    commentRequest: CommentCreateRequest,
):
    if not user:
        raise HTTPException(status_code=401, detail="Authentication failed")

    # Verify the post exists
    post = db.query(Post).filter(Post.id == commentRequest.post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Create a new comment
    new_comment = Comment(
        text=commentRequest.text,
        post_id=commentRequest.post_id,
        user_id=user.get("id"),
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    # Eagerly load the author relationship for the response
    comment_with_author = (
        db.query(Comment)
        .options(joinedload(Comment.author))
        .filter(Comment.id == new_comment.id)
        .first()
    )

    return comment_with_author
