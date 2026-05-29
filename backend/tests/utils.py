async def create_user(client, name):
    response = await client.post(
        "/api/users",
        json={"name": name},
    )

    assert response.status_code == 200

    data = response.json()

    assert "id" in data
    assert "api_key" in data

    return data