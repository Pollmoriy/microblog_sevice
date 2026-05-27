import pytest

@pytest.mark.asyncio
async def test_create_tweet(client):
    response = await client.post(
        "/api/tweets",
        json={
            "tweet_data": "hello world",
            "tweet_media_ids": []
        }
    )

    assert response.status_code == 201
    assert "tweet_id" in response.json()


@pytest.mark.asyncio
async def test_get_feed(client):
    response = await client.get("/api/tweets")

    assert response.status_code == 200
    assert "tweets" in response.json()