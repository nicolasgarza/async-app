from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import text, ForeignKey
from datetime import datetime
from pydantic import BaseModel
from uuid import UUID, uuid4
from typing import List

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
    created_at: datetime = Field(default_factory=datetime.utcnow,
                                          nullable=False,
                                          sa_column_kwargs={
                                              "server_default": text("current_timestamp(0)")
                                          })
    updated_at: datetime = Field(default_factory=datetime.utcnow,
                                          nullable=False,
                                          sa_column_kwargs={
                                              "server_default": text("current_timestamp(0)"),
                                              "onupdate": text("current_timestamp(0)")
                                          })

class User(SQLModel, table=True):
    __tablename__ = 'users'
    uuid: UUID = Field(default_factory=uuid4, primary_key=True, index=True, nullable=False,
                       sa_column_kwargs={"server_default": text("gen_random_uuid()"), "unique": True})
    username: str = Field(index=True, nullable=False, max_length=255)
    email: str = Field(index=True, nullable=False, max_length=255)
    hashed_password: str = Field(nullable=False)
    # Relationships
    posts: List["Post"] = Relationship(back_populates="author", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    comments: List["Comment"] = Relationship(back_populates="author", sa_relationship_kwargs={"cascade": "all, delete-orphan"})

class Post(SQLModel, table=True):
    __tablename__ = 'posts'
    uuid: UUID = Field(default_factory=uuid4, primary_key=True, index=True, nullable=False,
                       sa_column_kwargs={"server_default": text("gen_random_uuid()"), "unique": True})
    title: str = Field(nullable=False)
    content: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    author_uuid: UUID = Field(foreign_key="users.uuid", sa_column_kwargs={
        "foreign_key": ForeignKey("users.uuid", ondelete="CASCADE")
    })
    # Relationships
    author: User = Relationship(back_populates="posts")
    comments: List["Comment"] = Relationship(back_populates="post", sa_relationship_kwargs={"cascade": "all, delete-orphan"})

class Comment(SQLModel, table=True):
    __tablename__ = 'comments'
    uuid: UUID = Field(default_factory=uuid4, primary_key=True, index=True, nullable=False,
                       sa_column_kwargs={"server_default": text("gen_random_uuid()"), "unique": True})
    content: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    author_uuid: UUID = Field(foreign_key="users.uuid")
    post_uuid: UUID = Field(foreign_key="posts.uuid", sa_column_kwargs={
        "foreign_key": ForeignKey("posts.uuid", ondelete="CASCADE")
    })
    # Relationships
    author: User = Relationship(back_populates="comments")
    post: Post = Relationship(back_populates="comments")
