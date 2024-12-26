
from sqlalchemy import Column, Integer, String, column, Boolean, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(250), nullable=False)
    password = Column(String(250), nullable=False)
    email = Column(String(250), unique=True, nullable=False)
    profile_picture_url = Column(String(250), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    posts = relationship("Post", back_populates="owner")


# Post Model
class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(250), nullable=False)
    image_url = Column(String(250), nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # Foreign key to User
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    owner = relationship("User", back_populates="posts")