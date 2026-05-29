import io

import pytest

from test_helpers import create_user

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