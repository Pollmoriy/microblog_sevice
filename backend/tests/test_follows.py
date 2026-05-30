import pytest
from tests.test_helpers import create_user


@pytest.mark.asyncio
async def test_follow_user(client):
    user1 = await create_user(client, "A")
    user2 = await create_user(client, "B")

    response = await client.post(
        f"/api/users/{user2['id']}/follow",
        headers={"api-key": user1["api_key"]},
    )

    assert response.status_code == 200
    assert response.json()["result"] is True


@pytest.mark.asyncio
async def test_follow_self(client):
    user = await create_user(client, "A")

    response = await client.post(
        f"/api/users/{user['id']}/follow",
        headers={"api-key": user["api_key"]},
    )

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_double_follow(client):
    user1 = await create_user(client, "A")
    user2 = await create_user(client, "B")

    await client.post(
        f"/api/users/{user2['id']}/follow",
        headers={"api-key": user1["api_key"]},
    )

    response = await client.post(
        f"/api/users/{user2['id']}/follow",
        headers={"api-key": user1["api_key"]},
    )

    assert response.status_code == 400
