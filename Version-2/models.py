
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    email = Column(String(250), unique=True, nullable=False)
    profile_picture_url = Column(String(250), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    posts = relationship("Post", back_populates="owner")
    comments = relationship("Comment", back_populates="author")


# Post Model
class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(250), nullable=False)
    image_url = Column(String(250), nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # Foreign key to User
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    # Relationships
    owner = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    author = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")


