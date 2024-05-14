from uuid import UUID
from fastapi import HTTPException
from fastapi import status as http_status
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
import bcrypt

from app.blog.models import UserBase, UserCreate, UserUpdate, PostBase, PostCreate, CommentBase, CommentCreate
from app.core.models import User, Post, Comment

class BlogCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

    # User endpoints
    async def create_user(self, data: UserCreate) -> UserBase:
        hashed_password = bcrypt.hashpw(data.password.encode('utf-8'), bcrypt.gensalt())

        user = User(
            username=data.username,
            email=data.email,
            hashed_password=hashed_password.decode('utf-8') 
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
    
    async def get_user(self, user_uuid: str) -> UserBase:
        statement = select(User).where(User.uuid == user_uuid)
        result = await self.session.execute(statement)
        user = result.scalar_one_or_none()
        if user is None:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="User not found!"
            )
        return user
    
    async def update_user(self, user_uuid: str, data: UserUpdate) -> UserBase:
        statement = select(User).where(User.uuid == user_uuid)
        result = await self.session.execute(statement)
        user = result.scalar_one_or_none()
        if user is None:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="User not found!"
            )
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(user, key, value)

        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
    
    async def delete_user(self, user_uuid: str) -> bool:
        statement = delete(User).where(User.uuid == user_uuid)
        await self.session.execute(statement)
        await self.session.commit()
        return True
    
    # Post endpoints
    async def create_post(self, data: PostCreate, author_uuid: str) -> PostBase:
        post = Post(title=data.title, content=data.content, author_uuid=author_uuid)
        self.session.add(post)
        await self.session.commit()
        await self.session.refresh(post)
        return post
    
    async def get_post(self, post_uuid: str) -> PostBase:
        statement = select(Post).where(Post.uuid == post_uuid)
        result = await self.session.execute(statement)
        post = result.scalar_one_or_none()
        if post is None:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="Post not found!"
            )
        return post
    
    async def update_post(self, post_uuid: str, data: PostCreate) -> PostBase:
        statement = select(Post).where(Post.uuid == post_uuid)
        result = await self.session.execute(statement)
        post = result.scalar_one_or_none()
        if post is None:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="Post not found!"
            )
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(post, key, value)

        self.session.add(post)
        await self.session.commit()
        await self.session.refresh(post)
        return post
    
    async def delete_post(self, post_uuid: str) -> bool:
        statement = delete(Post).where(Post.uuid == post_uuid)
        await self.session.execute(statement)
        await self.session.commit()
        return True
    
    # Comment endpoints
    async def create_comment(self, data: CommentCreate, author_uuid: str) -> CommentBase:
        comment = Comment(content=data.content, post_id=data.post_id, author_uuid=author_uuid)
        self.session.add(comment)
        await self.session.commit()
        await self.session.refresh(comment)
        return comment

    async def get_comment(self, comment_uuid: str) -> CommentBase:
        statement = select(Comment).where(Comment.id == comment_uuid)
        result = await self.session.execute(statement)
        comment = result.scalar_one_or_none()
        if comment is None:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="Comment not found!"
            )
        return comment
    
    async def update_comment(self, comment_uuid: str, data: CommentCreate) -> CommentBase:
        statement = select(Comment).where(Comment.uuid == comment_uuid)
        result = await self.session.execute(statement)
        comment = result.scalar_one_or_none()
        if comment is None:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="Comment not found!"
            )
        
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(comment, key, value)

        self.session.add(comment)
        await self.session.commit()
        await self.session.refresh(comment)
        return comment
    
    async def delete_comment(self, comment_uuid: str) -> bool:
        statement = delete(Comment).where(Comment.uuid == comment_uuid)
        await self.session.execute(statement)
        await self.session.commit()
        return True
