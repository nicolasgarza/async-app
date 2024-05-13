from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, Integer, String, ForeignKey, text
from pydantic import BaseModel
from sqlalchemy.orm import relationship
from datetime import datetime
from uuid import UUID, uuid4

class HealthCheck(BaseModel):
    name: str
    version: str
    description: str

class StatusMessage(BaseModel):
    status: bool
    message: str

class UUIDModel(SQLModel):
    uuid: UUID = Field(default_factory=uuid4,
                       primary_key=True,
                       index=True,
                       nullable=False,
                       sa_column_kwargs={
                           "server_default": text("gen_random_uuid()"),
                           "unique": True
                       })

class TimestampModel(SQLModel):
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow,
                                          nullable=False,
                                          sa_column_kwargs={
                                              "server_default": text("current_timestamp(0)")
                                          })
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow,
                                          nullable=False,
                                          sa_column_kwargs={
                                              "server_default": text("current_timestamp(0)"),
                                              "onupdate": text("current_timestamp(0)")
                                          })

class UserBase(SQLModel):
    username: str = Field(index=True, nullable=False, max_length=255)
    email: str = Field(index=True, nullable=False, max_length=255)

class User(UserBase, table=True):
    __tablename__ = 'users'
    id: int = Field(default=None, primary_key=True)
    hashed_password: str = Field(nullable=False)
    # Relationships
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
