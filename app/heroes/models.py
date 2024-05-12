from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional, List

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserRead(UserBase):
    id: int

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class PostBase(BaseModel):
    title: str
    content: str

class PostRead(PostBase):
    id: int
    created_at: datetime
    author_id: int

class PostCreate(PostBase):
    pass

class CommentBase(BaseModel):
    content: str

class CommentRead(CommentBase):
    id: int
    created_at: datetime
    author_id: int
    post_id: int

class CommentCreate(CommentBase):
    post_id: int