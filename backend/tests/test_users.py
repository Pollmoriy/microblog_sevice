import pytest

from utils import create_user

@pytest.mark.asyncio
async def test_create_user(client):
    data = await create_user(client, "Polina")

    assert data["name"] == "Polina"


@pytest.mark.asyncio
async def test_get_me(client):
    user = await create_user(client, "A")

    response = await client.get(
        "/api/users/me",
        headers={"api-key": user["api_key"]},
    )

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_user_profile(client):
    user = await create_user(client, "A")

    response = await client.get(
        f"/api/users/{user['id']}",
        headers={"api-key": user["api_key"]},
    )

    assert response.status_code == 200