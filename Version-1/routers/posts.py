from typing import Annotated, List


from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Post
from schemas import PostCreateRequest, PostResponse, PostUpdateRequest

router = APIRouter()
router = APIRouter(
    prefix='/post',
    tags=['APIs of Posts of Social Media']
)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
db_dependency = Annotated[Session, Depends(get_db)]

@router.get('/read-posts/{user_id}', response_model=List[PostResponse])
def Read_all_posts_of_User(db: db_dependency,user_id: int):
    return db.query(Post).filter(Post.user_id == user_id).all()
@router.get('/read-posts/{id}', response_model=PostResponse)
def get_posts_by_ID(db: db_dependency ,id: int):
    return db.query(Post).filter(Post.id == id).first()


@router.post('/create-posts', status_code=201, response_model=PostResponse)
def create_post(
    post: PostCreateRequest,
    db: db_dependency,
    args: str = Query(None),  # Optional query parameter
    kwargs: str = Query(None)  # Optional query parameter
):
    print(f"args: {args}, kwargs: {kwargs}")  # Log or use args/kwargs if needed
    newPost = Post(
        text=post.text,
        image_url=post.image_url,
        user_id=post.user_id
    )
    db.add(newPost)
    db.commit()
    db.refresh(newPost)
    return newPost
@router.delete('/delete-posts/{id}', status_code=204)
def delete_post(db : db_dependency, id :int  ):
    post = db.query(Post).get(id)
    db.delete(post)
    db.commit()
    return {f" post with id: {id}  deleted successfully"}


@router.put('/update-posts', status_code=204)
def update_post(db: db_dependency, post : PostUpdateRequest):
    toUpdatepost = db.query(Post).get(post.id)
    if toUpdatepost is None:
        raise HTTPException(status_code=404, detail="post not found")
    toUpdatepost.text = post.text,
    toUpdatepost.image_url = post.image_url,
    db.add(toUpdatepost)
    db.commit()
    return {f" post with id: {post.id} updated successfully"}
