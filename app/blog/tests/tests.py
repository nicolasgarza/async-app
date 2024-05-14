import pytest
from httpx import AsyncClient
from sqlalchemy import insert, select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import User, Post

# fixtures

@pytest.fixture
async def test_user(async_session: AsyncSession):
    user_data = {
        "username": "test_user",
        "email": "test@example.com",
        "hashed_password": "fakehashedpassword"
    }
    user_stmt = insert(User).values(user_data)
    result = await async_session.exec(user_stmt)
    await async_session.commit()
    user_uuid = result.inserted_primary_key[0]
    
    yield user_uuid

    # Delete all posts for the user first
    await async_session.exec(delete(Post).where(Post.author_uuid == user_uuid))
    await async_session.commit()

    # Now delete the user
    await async_session.exec(delete(User).where(User.uuid == user_uuid))
    await async_session.commit()

@pytest.fixture
async def test_post(async_session: AsyncSession, test_user):
    post_data = {
        "title": "Test Post",
        "content": "This is a test post",
        "author_uuid": test_user
    }
    post_stmt = insert(Post).values(post_data)
    result = await async_session.exec(post_stmt)
    await async_session.commit()
    post_uuid = result.inserted_primary_key[0]
    yield post_uuid
    await async_session.exec(delete(Post).where(Post.uuid == post_uuid))
    await async_session.commit()

# tests

@pytest.mark.asyncio
async def test_create_user(
        async_client: AsyncClient,
        async_session: AsyncSession,
        test_data: dict
):
    payload = test_data["case_create"]["payload"]
    response = await async_client.post("/users", json=payload)

    assert response.status_code == 201

    got = response.json()
    want = test_data["case_create"]["want"]

    for k, v in want.items():
        assert got[k] == v

    assert 'uuid' in got

    statement = select(User).where(User.uuid == got["uuid"])
    results = await async_session.exec(statement=statement)
    user = results.scalar_one()

    for k, v in want.items():
        assert getattr(user, k) == v

@pytest.mark.asyncio
async def test_get_user(
    async_client: AsyncClient,
    async_session: AsyncSession,
    test_data: dict
):
    testing_data = test_data["case_create"]["payload"].copy()
    del testing_data["password"]
    testing_data["hashed_password"] = "securePassword123"
    user_data = testing_data
    statement = insert(User).values(user_data)
    result = await async_session.exec(statement)
    await async_session.commit()
    user_id = result.inserted_primary_key[0]

    response = await async_client.get(f"/users/{user_id}")
    assert response.status_code == 200

    got = response.json()
    want = test_data["case_get"]["want"]

    for k, v in want.items():
        assert got[k] == v

@pytest.mark.asyncio
async def test_update_user(
    async_client: AsyncClient,
    async_session: AsyncSession,
    test_data: dict
):
    testing_data = test_data["case_create"]["payload"].copy()
    del testing_data["password"]
    testing_data["hashed_password"] = "securePassword123"
    user_data = testing_data
    statement = insert(User).values(user_data)
    result = await async_session.exec(statement)
    await async_session.commit()
    user_id = result.inserted_primary_key[0]

    payload = test_data["case_patch"]["payload"]
    response = await async_client.patch(f"/users/{user_id}", json=payload)
    assert response.status_code == 200

    got = response.json()
    want = test_data["case_patch"]["want"]

    for k, v in want.items():
        assert got[k] == v

@pytest.mark.asyncio
async def test_delete_user(
    async_client: AsyncClient,
    async_session: AsyncSession,
    test_data: dict
):
    testing_data = test_data["case_create"]["payload"].copy()
    del testing_data["password"]
    testing_data["hashed_password"] = "securePassword123"
    user_data = testing_data
    statement = insert(User).values(user_data)
    result = await async_session.exec(statement)
    await async_session.commit()
    user_uuid = result.inserted_primary_key[0]

    response = await async_client.delete(f"/users/{user_uuid}")
    assert response.status_code == 200

    got = response.json()
    want = test_data["case_delete"]["want"]

    for k, v in want.items():
        assert got[k] == v

    statement = select(User).where(User.uuid == user_uuid)
    results = await async_session.exec(statement)
    user = results.scalar_one_or_none()

    assert user is None

@pytest.mark.asyncio
async def test_create_post(async_client: AsyncClient, async_session: AsyncSession, test_data: dict, test_user):
    payload = test_data["post_case_create"]["payload"]
    response = await async_client.post(f"/posts?author_uuid={test_user}", json=payload)
    
    assert response.status_code == 201
    got = response.json()
    want = test_data["post_case_create"]["want"]
    
    for k, v in want.items():
        assert got[k] == v

    assert 'uuid' in got

    # Check post was inserted into the database
    statement = select(Post).where(Post.uuid == got["uuid"])
    results = await async_session.exec(statement=statement)
    post = results.scalar_one()
    
    for k, v in want.items():
        assert getattr(post, k) == v

@pytest.mark.asyncio
async def test_get_post_by_id(async_client: AsyncClient, async_session: AsyncSession, test_data: dict, test_post):
    response = await async_client.get(f"/posts/{test_post}")
    
    assert response.status_code == 200
    got = response.json()
    want = test_data["post_case_get"]["want"]
    
    for k, v in want.items():
        assert got[k] == v

@pytest.mark.asyncio
async def test_update_post_by_id(async_client: AsyncClient, async_session: AsyncSession, test_data: dict, test_post):
    payload = test_data["post_case_patch"]["payload"]
    response = await async_client.patch(f"/posts/{test_post}", json=payload)
    
    assert response.status_code == 200
    got = response.json()
    want = test_data["post_case_patch"]["want"]
    
    for k, v in want.items():
        assert got[k] == v

@pytest.mark.asyncio
async def test_delete_post_by_id(async_client: AsyncClient, async_session: AsyncSession, test_data: dict, test_post):
    response = await async_client.delete(f"/posts/{test_post}")
    
    assert response.status_code == 200
    got = response.json()
    want = test_data["post_case_delete"]["want"]
    
    assert got == want
    
    statement = select(Post).where(Post.uuid == test_post)
    results = await async_session.exec(statement)
    post = results.scalar_one_or_none()
    
    assert post is None
