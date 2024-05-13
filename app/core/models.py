from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class UserBase(SQLModel):
    username: str = Field(index=True, nullable=False, max_length=255)
    email: str = Field(index=True, nullable=False, max_length=255)

class User(UserBase, table=True):
    __tablename__ = 'users'
    id: int = Field(default=None, primary_key=True)
    hashed_password: str = Field(nullable=False)
    # Define relationships using Relationship
    posts: list["Post"] = Relationship(back_populates="author", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    comments: list["Comment"] = Relationship(back_populates="author", sa_relationship_kwargs={"cascade": "all, delete-orphan"})

class Post(SQLModel, table=True):
    __tablename__ = 'posts'
    id: int = Field(default=None, primary_key=True)
    title: str = Field(nullable=False)
    content: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    author_id: int = Field(foreign_key="users.id")
    # Relationships
    author: User = Relationship(back_populates="posts")
    comments: list["Comment"] = Relationship(back_populates="post", sa_relationship_kwargs={"cascade": "all, delete-orphan"})

class Comment(SQLModel, table=True):
    __tablename__ = 'comments'
    id: int = Field(default=None, primary_key=True)
    content: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    author_id: int = Field(foreign_key="users.id")
    post_id: int = Field(foreign_key="posts.id")
    # Relationships
    author: User = Relationship(back_populates="comments")
    post: Post = Relationship(back_populates="comments")
