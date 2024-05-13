from sqlmodel import SQLModel, Field, Relationship
from pydantic import EmailStr
from typing import Optional, List
from datetime import datetime
from uuid import UUID

from app.core.models import UUIDModel, TimestampModel

class UserBase(SQLModel, UUIDModel, TimestampModel):
    username: str = Field(index=True, nullable=False, max_length=255)
    email: EmailStr

class UserRead(UserBase):
    pass  

class UserCreate(UserBase):
    password: str

class UserUpdate(SQLModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class PostBase(SQLModel, UUIDModel, TimestampModel):
    title: str = Field(nullable=False, max_length=255)
    content: str = Field(nullable=False, max_length=2048)
    author_id: UUID = Field(foreign_key="user.uuid")

class PostRead(PostBase):
    pass

class PostCreate(PostBase):
    pass  

class CommentBase(SQLModel, UUIDModel, TimestampModel):
    content: str = Field(nullable=False, max_length=1024)
    author_id: UUID = Field(foreign_key="user.uuid")
    post_id: UUID = Field(foreign_key="post.uuid")

class CommentRead(CommentBase):
    pass

class CommentCreate(CommentBase):
    pass
