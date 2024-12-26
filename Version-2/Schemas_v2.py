from datetime import datetime

from pydantic import BaseModel
from schemas import UserBase


class CommentBase(BaseModel):
    text: str

class CommentCreateRequest(CommentBase):
    post_id: int



class CommentsResponse(CommentBase):
    id: int
    created_at: datetime
    author: UserBase

    class Config:
        orm_mode = True

