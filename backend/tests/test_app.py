import io

import pytest


async def create_user(client, name):
    response = await client.post("/api/users", json={"name": name})

    assert response.status_code == 200

    data = response.json()

    assert "id" in data
    assert "api_key" in data

    return data


@pytest.mark.asyncio
async def test_create_user(client):
    data = await create_user(client, "Polina")

    assert data["name"] == "Polina"


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

    data = response.json()

    assert "tweet_id" in data


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

    assert tweet_response.status_code == 201

    tweet_id = tweet_response.json()["tweet_id"]

    response = await client.post(
        f"/api/tweets/{tweet_id}/likes",
        headers={"api-key": user2["api_key"]},
    )

    assert response.status_code == 200
    assert response.json()["result"] is True


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
async def test_feed(client):
    user1 = await create_user(client, "A")
    user2 = await create_user(client, "B")

    follow_response = await client.post(
        f"/api/users/{user2['id']}/follow",
        headers={"api-key": user1["api_key"]},
    )

    assert follow_response.status_code == 200

    tweet_response = await client.post(
        "/api/tweets",
        json={
            "tweet_data": "feed tweet",
            "tweet_media_ids": [],
        },
        headers={"api-key": user2["api_key"]},
    )

    assert tweet_response.status_code == 201

    response = await client.get(
        "/api/tweets",
        headers={"api-key": user1["api_key"]},
    )

    assert response.status_code == 200

    data = response.json()

    assert "tweets" in data
    assert len(data["tweets"]) >= 1


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

    assert tweet_response.status_code == 201

    tweet_id = tweet_response.json()["tweet_id"]

    response = await client.delete(
        f"/api/tweets/{tweet_id}",
        headers={"api-key": user["api_key"]},
    )

    assert response.status_code == 200
    assert response.json()["result"] is True


@pytest.mark.asyncio
async def test_delete_foreign_tweet_forbidden(client):
    user1 = await create_user(client, "A")
    user2 = await create_user(client, "B")

    tweet_response = await client.post(
        "/api/tweets",
        json={
            "tweet_data": "not yours",
            "tweet_media_ids": [],
        },
        headers={"api-key": user1["api_key"]},
    )

    assert tweet_response.status_code == 201

    tweet_id = tweet_response.json()["tweet_id"]

    response = await client.delete(
        f"/api/tweets/{tweet_id}",
        headers={"api-key": user2["api_key"]},
    )

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_upload_media(client):
    user = await create_user(client, "A")

    file = io.BytesIO(b"test image content")

    response = await client.post(
        "/api/medias",
        files={"file": ("test.png", file, "image/png")},
        headers={"api-key": user["api_key"]},
    )

    assert response.status_code == 201

    data = response.json()

    assert "media_id" in data


@pytest.mark.asyncio
async def test_missing_api_key(client):
    response = await client.post(
        "/api/tweets",
        json={
            "tweet_data": "fail",
            "tweet_media_ids": [],
        },
    )

    assert response.status_code in [401, 422]


@pytest.mark.asyncio
async def test_like_nonexistent_tweet(client):
    user = await create_user(client, "A")

    response = await client.post(
        "/api/tweets/999999/likes",
        headers={"api-key": user["api_key"]},
    )

    assert response.status_code == 404


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

    assert tweet_response.status_code == 201

    tweet_id = tweet_response.json()["tweet_id"]

    first_like = await client.post(
        f"/api/tweets/{tweet_id}/likes",
        headers={"api-key": user2["api_key"]},
    )

    assert first_like.status_code == 200

    response = await client.post(
        f"/api/tweets/{tweet_id}/likes",
        headers={"api-key": user2["api_key"]},
    )

    assert response.status_code == 400


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

    first_follow = await client.post(
        f"/api/users/{user2['id']}/follow",
        headers={"api-key": user1["api_key"]},
    )

    assert first_follow.status_code == 200

    response = await client.post(
        f"/api/users/{user2['id']}/follow",
        headers={"api-key": user1["api_key"]},
    )

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_get_me(client):
    user = await create_user(client, "A")

    response = await client.get(
        "/api/users/me",
        headers={"api-key": user["api_key"]},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["user"]["id"] == user["id"]


@pytest.mark.asyncio
async def test_get_user_profile(client):
    user = await create_user(client, "A")

    response = await client.get(
        f"/api/users/{user['id']}",
        headers={"api-key": user["api_key"]},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["user"]["id"] == user["id"]
