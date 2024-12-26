from typing import Optional, List
from pydantic import BaseModel

class PostSummary(BaseModel):
    id: int
    text: str
    image_url: Optional[str]

    class Config:
        from_attributes = True  # Updated from orm_mode

class UserProfileResponse(BaseModel):
    id: int
    name: str
    email: str
    profile_picture_url: Optional[str]
    follower_count: int
    following_count: int
    posts: List[PostSummary]

    class Config:
        from_attributes = True  # Updated from orm_mode
