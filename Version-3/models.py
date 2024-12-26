
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), unique=True, nullable=False)
    hashed_password = Column(String(250), nullable=False)
    profile_picture_url = Column(String(250), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    followers_count = Column(Integer, default=0)
    following_count = Column(Integer, default=0)

    # Relationships
    posts = relationship("Post", back_populates="owner", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="author", cascade="all, delete-orphan")
    likes = relationship("Like", back_populates="user", cascade="all, delete-orphan")
    followers = relationship(
        "Follow",
        foreign_keys="[Follow.followed_id]",
        back_populates="followed",
        cascade="all, delete-orphan",
    )
    following = relationship(
        "Follow",
        foreign_keys="[Follow.follower_id]",
        back_populates="follower",
        cascade="all, delete-orphan",
    )

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from database import Base

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(500), nullable=False)
    image_url = Column(String(250), nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    like_count = Column(Integer, default=0)
    comments_count = Column(Integer, default=0)

    # Relationships
    owner = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
    likes = relationship("Like", back_populates="post", cascade="all, delete-orphan")




class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(500), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    author = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")


class Like(Base):
    __tablename__ = 'likes'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="likes")
    post = relationship("Post", back_populates="likes")


class Follow(Base):
    __tablename__ = 'follows'

    id = Column(Integer, primary_key=True, index=True)
    follower_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    followed_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    follower = relationship("User", foreign_keys=[follower_id], back_populates="following")
    followed = relationship("User", foreign_keys=[followed_id], back_populates="followers")


