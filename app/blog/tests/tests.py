import pytest
from httpx import AsyncClient
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.blog.models import UserCreate
from app.core.models import User

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
    testing_data = test_data["case_create"]["payload"]
    del testing_data["password"]
    testing_data["hashed_password"] = "securePassword123"
    user_data = test_data["case_create"]["payload"]
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

# @pytest.mark.asyncio
# async def test_update_user(
#     async_client: AsyncClient,
#     async_session: AsyncSession,
#     test_data: dict
# ):
#     user_data = test_data["case_create"]["want"]
#     statement = insert(User).values(user_data)
#     result = await async_session.exec(statement)
#     await async_session.commit()
#     user_id = result.inserted_primary_key[0]

#     payload = test_data["case_patch"]["payload"]
#     response = await async_client.patch(f"/users/{user_id}", json=payload)
#     assert response.status_code == 200

#     got = response.json()
#     want = test_data["case_patch"]["want"]

#     for k, v in want.items():
#         assert got[k] == v

# @pytest.mark.asyncio
# async def test_delete_user(
#     async_client: AsyncClient,
#     async_session: AsyncSession,
#     test_data: dict
# ):
#     user_data = test_data["case_create"]["want"]
#     statement = insert(User).values(user_data)
#     result = await async_session.exec(statement)
#     await async_session.commit()
#     user_id = result.inserted_primary_key[0]

#     response = await async_client.delete(f"/users/{user_id}")
#     assert response.status_code == 200

#     got = response.json()
#     want = test_data["case_delete"]["want"]

#     for k, v in want.items():
#         assert got[k] == v

#     statement = select(User).where(User.id == user_id)
#     results = await async_session.exec(statement)
#     user = results.scalar_one_or_none()

#     assert user is None
