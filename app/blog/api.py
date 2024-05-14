from fastapi import APIRouter, Depends, HTTPException
from fastapi import status as http_status
from sqlalchemy.ext.asyncio import AsyncSession
from app.blog.crud import BlogCRUD
from app.blog.dependencies import get_blog_crud
from app.blog.models import UserCreate, UserRead, UserUpdate, PostCreate, PostRead, CommentCreate, CommentRead
from app.core.models import StatusMessage

router = APIRouter()

# User endpoints
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
    "/users/{user_uuid}",
    response_model=UserRead,
    status_code=http_status.HTTP_200_OK
)
async def get_user_by_id(
    user_uuid: str, 
    crud: BlogCRUD = Depends(get_blog_crud)
):
    user = await crud.get_user(user_uuid=user_uuid)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.patch(
    "/users/{user_uuid}",
    response_model=UserRead,
    status_code=http_status.HTTP_200_OK
)
async def update_user_by_id(
    user_uuid: str, 
    data: UserUpdate, 
    crud: BlogCRUD = Depends(get_blog_crud)
):
    user = await crud.update_user(user_uuid=user_uuid, data=data)
    return user

@router.delete(
    "/users/{user_uuid}",
    response_model=StatusMessage,
    status_code=http_status.HTTP_200_OK
)
async def delete_user_by_id(
    user_uuid: str,
    crud: BlogCRUD = Depends(get_blog_crud)
):
    await crud.delete_user(user_uuid=user_uuid)
    return {"status": True, "message": "User has been deleted!"}

# Post endpoints
@router.post(
    "/posts",
    response_model=PostRead,
    status_code=http_status.HTTP_201_CREATED
)
async def create_post(
    data: PostCreate,
    author_uuid: str, 
    crud: BlogCRUD = Depends(get_blog_crud)
):
    post = await crud.create_post(data=data, author_uuid=author_uuid)
    return post

@router.get(
    "/posts/{post_uuid}",
    response_model=PostRead,
    status_code=http_status.HTTP_200_OK
)
async def get_post_by_id(
    post_uuid: str,
    crud: BlogCRUD = Depends(get_blog_crud)
):
    post = await crud.get_post(post_uuid=post_uuid)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.patch(
    "/posts/{post_uuid}",
    response_model=PostRead,
    status_code=http_status.HTTP_200_OK
)
async def update_post_by_id(
    post_uuid: str,
    data: PostCreate,
    crud: BlogCRUD = Depends(get_blog_crud)
):
    post = await crud.update_post(post_uuid=post_uuid, data=data)
    return post

@router.delete(
    "/posts/{post_id}",
    response_model=StatusMessage,
    status_code=http_status.HTTP_200_OK
)
async def delete_post_by_id(
    post_uuid: str,
    crud: BlogCRUD = Depends(get_blog_crud)
):
    await crud.delete_post(post_uuid=post_uuid)
    return {"status": True, "message": "Post has been deleted"}

# Comment endpoints
@router.post(
    "/comments",
    response_model=CommentRead,
    status_code=http_status.HTTP_201_CREATED
)
async def create_comment(
    data: CommentCreate,
    author_uuid: str,
    crud: BlogCRUD = Depends(get_blog_crud)
):
    comment = await crud.create_comment(data=data, author_uuid=author_uuid)
    return comment

@router.get(
    "/comments/{comment_uuid}",
    response_model=CommentRead,
    status_code=http_status.HTTP_200_OK
)
async def get_comment_by_id(
    comment_uuid: str,
    crud: BlogCRUD = Depends(get_blog_crud)
):
    comment = await crud.get_comment(comment_uuid=comment_uuid)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment

@router.patch(
    "/comments/{comment_uuid}",
    response_model=CommentRead,
    status_code=http_status.HTTP_200_OK
)
async def update_comment_by_id(
    comment_uuid: str,
    data: CommentCreate,
    crud: BlogCRUD = Depends(get_blog_crud)
):
    comment = await crud.update_comment(comment_uuid=comment_uuid, data=data)
    return comment

@router.delete(
    "/comments/{comment_uuid}",
    response_model=StatusMessage,
    status_code=http_status.HTTP_200_OK
)
async def delete_comment_by_id(
    comment_uuid: str,
    crud: BlogCRUD = Depends(get_blog_crud)
):
    await crud.delete_comment(comment_uuid=comment_uuid)
    return {"status": True, "message": "Comment has been deleted"}
