from fastapi import APIRouter, Depends, HTTPException
from fastapi import status as http_status
from sqlalchemy.ext.asyncio import AsyncSession
from app.heroes.crud import BlogCRUD
from app.heroes.dependencies import get_blog_crud
from app.heroes.models import UserCreate, UserRead, UserUpdate, PostCreate, PostRead, CommentCreate, CommentRead
from app.core.models import StatusMessage

router = APIRouter()

@router.post(
    "/users",  
    response_model=UserRead,
    status_code=http_status.HTTP_201_CREATED
)
async def create_user(
    data: UserCreate,
    crud: BlogCRUD = Depends(get_blog_crud)
):
    user = await crud.create_user(data=data)
    return user

@router.get(
    "/users/{user_id}",
    response_model=UserRead,
    status_code=http_status.HTTP_200_OK
)
async def get_user_by_id(
    user_id: int, 
    crud: BlogCRUD = Depends(get_blog_crud)
):
    user = await crud.get_user(user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.patch(
    "/users/{user_id}",
    response_model=UserRead,
    status_code=http_status.HTTP_200_OK
)
async def update_user_by_id(
    user_id: int, 
    data: UserUpdate, 
    crud: BlogCRUD = Depends(get_blog_crud)
):
    user = await crud.update_user(user_id=user_id, data=data)
    return user

# User delete endpoint
@router.delete(
    "/users/{user_id}",
    response_model=StatusMessage,
    status_code=http_status.HTTP_200_OK
)
async def delete_user_by_id(
    user_id: int,
    crud: BlogCRUD = Depends(get_blog_crud)
):
    await crud.delete_user(user_id=user_id)
    return {"status": True, "message": "User has been deleted"}

# Post creation endpoint
@router.post(
    "/posts",
    response_model=PostRead,
    status_code=http_status.HTTP_201_CREATED
)
async def create_post(
    data: PostCreate,
    author_id: int, 
    crud: BlogCRUD = Depends(get_blog_crud)
):
    post = await crud.create_post(data=data, author_id=author_id)
    return post

# Comment creation endpoint
@router.post(
    "/comments",
    response_model=CommentRead,
    status_code=http_status.HTTP_201_CREATED
)
async def create_comment(
    data: CommentCreate,
    author_id: int,
    crud: BlogCRUD = Depends(get_blog_crud)
):
    comment = await crud.create_comment(data=data, author_id=author_id)
    return comment