from datetime import datetime

from pydantic import BaseModel
from sqlalchemy import  DateTime

from typing import Optional

class UserBase(BaseModel):
    name: str
    email: str
    profile_picture_url: Optional[str] = None  # Optional field for profile picture URL


# Request Schema for Creating a User
class UserCreateRequest(UserBase):
    password: str  # Password field for registration


# Response Schema for User
class UserResponse(UserBase):
    id: int  # Include the user's ID in the response
    is_active: bool  # Include the active status

    class Config:
        from_attributes = True  # Use from_attributes for Pydantic V2


# Base Schema for Post
class PostBase(BaseModel):
    text: str
    image_url: Optional[str] = None  # Optional image URL


# Request Schema for Creating a Post
class PostCreateRequest(PostBase):
    user_id: int
class PostUpdateRequest(PostBase):
    id : int


# Response Schema for Post
class PostResponse(BaseModel):
    id: int
    text: str
    image_url: Optional[str] = None
    created_at: datetime  # Use Python's datetime
    owner: "UserResponse"  # Reference to another Pydantic schema

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True