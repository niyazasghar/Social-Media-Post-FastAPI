from datetime import datetime

from pydantic import BaseModel


from typing import Optional

class UserBase(BaseModel):
    name: str
    email: str



class UserCreateRequest(UserBase):
    password: str


# Response Schema for User
class UserResponse(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True


# Base Schema for Post
class PostBase(BaseModel):
    text: str
    image_url: Optional[str] = None



class PostCreateRequest(PostBase):
    user_id: int
class PostUpdateRequest(PostBase):
    id : int
    updated_at: Optional[str] = None


# Response Schema for Post
class PostResponse(BaseModel):
    id: int
    text: str
    image_url: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime]
    owner: Optional[UserResponse]  # Use None if owner is not loaded

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True