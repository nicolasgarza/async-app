from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.blog.crud import BlogCRUD

async def get_blog_crud(
        session: AsyncSession = Depends(get_async_session)
) -> BlogCRUD:
    return BlogCRUD(session=session)