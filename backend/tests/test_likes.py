import pytest

from test_helpers import create_user

@pytest.mark.asyncio
async def test_like_tweet(client):
    user1 = await create_user(client, "A")
    user2 = await create_user(client, "B")

    tweet_response = await client.post(
        "/api/tweets",
        json={
            "tweet_data": "like me",
            "tweet_media_ids": [],
        },
        headers={"api-key": user1["api_key"]},
    )

    tweet_id = tweet_response.json()["tweet_id"]

    response = await client.post(
        f"/api/tweets/{tweet_id}/likes",
        headers={"api-key": user2["api_key"]},
    )

    assert response.status_code == 200
    assert response.json()["result"] is True


@pytest.mark.asyncio
async def test_double_like(client):
    user1 = await create_user(client, "A")
    user2 = await create_user(client, "B")

    tweet_response = await client.post(
        "/api/tweets",
        json={
            "tweet_data": "like me",
            "tweet_media_ids": [],
        },
        headers={"api-key": user1["api_key"]},
    )

    tweet_id = tweet_response.json()["tweet_id"]

    await client.post(
        f"/api/tweets/{tweet_id}/likes",
        headers={"api-key": user2["api_key"]},
    )

    response = await client.post(
        f"/api/tweets/{tweet_id}/likes",
        headers={"api-key": user2["api_key"]},
    )

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_like_nonexistent_tweet(client):
    user = await create_user(client, "A")

    response = await client.post(
        "/api/tweets/999999/likes",
        headers={"api-key": user["api_key"]},
    )

    assert response.status_code == 404