from sqlmodel import SQLModel, Field, Relationship
from pydantic import EmailStr
from typing import Optional, List
from datetime import datetime

class UserBase(SQLModel):
    username: str = Field(index=True, nullable=False, max_length=255)
    email: EmailStr

class UserRead(UserBase):
    id: int = Field(default=None, primary_key=True)

class UserCreate(UserBase):
    password: str 

class UserUpdate(SQLModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class PostBase(SQLModel):
    title: str = Field(nullable=False, max_length=255)
    content: str = Field(nullable=False, max_length=2048)

class PostRead(PostBase):
    id: int = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    author_id: int = Field(foreign_key="users.id")

class PostCreate(PostBase):
    pass  

class CommentBase(SQLModel):
    content: str = Field(nullable=False, max_length=1024)

class CommentRead(CommentBase):
    id: int = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    author_id: int = Field(foreign_key="users.id")
    post_id: int = Field(foreign_key="posts.id")

class CommentCreate(CommentBase):
    post_id: int
