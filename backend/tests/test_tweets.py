import pytest

from conftest import create_user


@pytest.mark.asyncio
async def test_create_tweet(client):
    user = await create_user(client, "Polina")

    response = await client.post(
        "/api/tweets",
        json={
            "tweet_data": "hello test tweet",
            "tweet_media_ids": [],
        },
        headers={"api-key": user["api_key"]},
    )

    assert response.status_code == 201


@pytest.mark.asyncio
async def test_feed(client):
    user1 = await create_user(client, "A")
    user2 = await create_user(client, "B")

    await client.post(
        f"/api/users/{user2['id']}/follow",
        headers={"api-key": user1["api_key"]},
    )

    await client.post(
        "/api/tweets",
        json={
            "tweet_data": "feed tweet",
            "tweet_media_ids": [],
        },
        headers={"api-key": user2["api_key"]},
    )

    response = await client.get(
        "/api/tweets",
        headers={"api-key": user1["api_key"]},
    )

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_delete_own_tweet(client):
    user = await create_user(client, "A")

    tweet_response = await client.post(
        "/api/tweets",
        json={
            "tweet_data": "to delete",
            "tweet_media_ids": [],
        },
        headers={"api-key": user["api_key"]},
    )

    tweet_id = tweet_response.json()["tweet_id"]

    response = await client.delete(
        f"/api/tweets/{tweet_id}",
        headers={"api-key": user["api_key"]},
    )

    assert response.status_code == 200