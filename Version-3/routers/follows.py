from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import SessionLocal
from models import User, Follow
from routers.auth import get_current_user
from schemas import userFollower

router = APIRouter(
    prefix="/follows",
    tags=[" APIs related to followers of Usres"]
)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.post("/follow/{user_id}")
def follow_user(user_id: int, user: user_dependency, db: db_dependency):
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")

    followed_user = db.query(User).filter(User.id == user_id).first()
    if not followed_user:
        raise HTTPException(status_code=404, detail="User not found")

    follow = db.query(Follow).filter(Follow.follower_id == user["id"], Follow.followed_id == user_id).first()
    if follow:
        raise HTTPException(status_code=400, detail="You are already following this user")

    # Add a new follow
    new_follow = Follow(follower_id=user["id"], followed_id=user_id)
    db.add(new_follow)

    # Increment follower and following counts
    followed_user.followers_count += 1
    db.query(User).filter(User.id == user["id"]).update({"following_count": User.following_count + 1})
    db.commit()

    return {"message": "User followed successfully", "follower_count": followed_user.followers_count}


@router.delete("/unfollow/{user_id}")
def unfollow_user(user_id: int, user: user_dependency, db: db_dependency):
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")

    followed_user = db.query(User).filter(User.id == user_id).first()
    if not followed_user:
        raise HTTPException(status_code=404, detail="User not found")

    follow = db.query(Follow).filter(Follow.follower_id == user["id"], Follow.followed_id == user_id).first()
    if not follow:
        raise HTTPException(status_code=404, detail="You are not following this user")

    # Remove the follow
    db.delete(follow)

    # Decrement follower and following counts
    followed_user.followers_count -= 1
    db.query(User).filter(User.id == user["id"]).update({"following_count": User.following_count - 1})
    db.commit()

    return {"message": "User unfollowed successfully", "follower_count": followed_user.followers_count}

@router.get("/get_followers", response_model=List[userFollower])
def get_followers(db:  db_dependency, user: user_dependency):
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")

    # Fetch followers
    followers = db.query(Follow).filter(Follow.followed_id == user["id"]).all()

    # Fetch follower user details (only user_name)
    follower_users = (
        db.query(User.name)
        .filter(User.id.in_([follow.follower_id for follow in followers]))
        .all()
    )

    # Format the response
    return [{"user_name": follower.name} for follower in follower_users]