from uuid import UUID
from fastapi import HTTPException
from fastapi import status as http_status
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.heroes.models import UserBase, UserCreate, UserUpdate, PostBase, PostCreate, CommentBase, CommentCreate
from app.core.models import User, Post, Comment

class BlogCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

    # User endpoints
    async def create_user(self, data: UserCreate) -> UserBase:
        user = User(
            username=data.username,
            email=data.email,
            hashed_password=data.password
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
    
    async def get_user(self, user_id: int) -> UserBase:
        statement = select(User).where(User.id == user_id)
        result = await self.session.execute(statement)
        user = result.scalar_one_or_none()
        if user is None:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="User not found!"
            )
        return user
    
    async def update_user(self, user_id: int, data: UserUpdate) -> UserBase:
        statement = select(User).where(User.id == user_id)
        result = await self.session.execute(statement)
        user = result.scalar_one_or_none()
        if user is None:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="User not found!"
            )
        update_data = data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(user, key, value)

        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
    
    async def delete_user(self, user_id: int) -> bool:
        statement = delete(User).where(User.id == user_id)
        await self.session.execute(statement)
        await self.session.commit()
        return True
    
    # Post endpoints
    async def create_post(self, data: PostCreate, author_id: int) -> PostBase:
        post = Post(title=data.title, content=data.content, author_id=author_id)
        self.session.add(post)
        await self.session.commit()
        await self.session.refresh(post)
        return post
    
    async def get_post(self, post_id: int) -> PostBase:
        statement = select(Post).where(Post.id == post_id)
        result = await self.session.execute(statement)
        post = result.scalar_one_or_none()
        if post is None:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="Post not found!"
            )
        return post
    
    async def update_post(self, post_id: int, data: PostCreate) -> PostBase:
        statement = select(Post).where(Post.id == post_id)
        result = await self.session.execute(statement)
        post = result.scalar_one_or_none()
        if post is None:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="Post not found!"
            )
        update_data = data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(post, key, value)

        self.session.add(post)
        await self.session.commit()
        await self.session.refresh(post)
        return post
    
    async def delete_post(self, post_id: int) -> bool:
        statement = delete(Post).where(Post.id == post_id)
        await self.session.execute(statement)
        await self.session.commit()
        return True
    
    # Comment endpoints
    async def create_comment(self, data: CommentCreate, author_id: int) -> CommentBase:
        comment = Comment(content=data.content, post_id=data.post_id, author_id=author_id)
        self.session.add(comment)
        await self.session.commit()
        await self.session.refresh(comment)
        return comment

    async def get_comment(self, comment_id: int) -> CommentBase:
        statement = select(Comment).where(Comment.id == comment_id)
        result = await self.session.execute(statement)
        comment = result.scalar_one_or_none()
        if comment is None:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="Comment not found!"
            )
        return comment
    
    async def update_comment(self, comment_id: int, data: CommentCreate) -> CommentBase:
        statement = select(Comment).where(Comment.id == comment_id)
        result = await self.session.execute(statement)
        comment = result.scalar_one_or_none()
        if comment is None:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="Comment not found!"
            )
        
        update_data = data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(comment, key, value)

        self.session.add(comment)
        await self.session.commit()
        await self.session.refresh(comment)
        return comment
    
    async def delete_comment(self, comment_id: int) -> bool:
        statement = delete(Comment).where(Comment.id == comment_id)
        await self.session.execute(statement)
        await self.session.commit()
        return True
