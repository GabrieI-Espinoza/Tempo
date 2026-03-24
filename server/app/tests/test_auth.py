import pytest


@pytest.mark.asyncio
async def test_register_user(client):
    # First create user
    response = await client.post(
        "/auth/register",
        json={
            "email": "johndoe@example.com",
            "password": "strongpassword123",
            "first_name": "John",
            "last_name": "Doe",
        },
    )
    # Check if the response status code is 201 Created
    assert response.status_code == 201

    # Parse the JSON response from the server
    data = response.json()
    # Check if the response contains an access token and the correct user information
    assert "access_token" in data
    assert data["user"]["email"] == "johndoe@example.com"


@pytest.mark.asyncio
async def test_login_user(client):
    # First create user
    await client.post(
        "/auth/register",
        json={
            "email": "johndoe@example.com",
            "password": "strongpassword123",
            "first_name": "John",
            "last_name": "Doe",
        },
    )
    # Attempt to login with user credentials
    response = await client.post(
        "/auth/login",
        json={
            "email": "johndoe@example.com",
            "password": "strongpassword123",
        },
    )
    # Check for status 200 OK
    assert response.status_code == 200
    # Ensure token is provided in response
    assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_get_current_user(client):
    # First create user
    register_response = await client.post(
        "/auth/register",
        json={
            "email": "johndoe@example.com",
            "password": "strongpassword123",
            "first_name": "John",
            "last_name": "Doe",
        },
    )
    # Extract token from registration response
    token = register_response.json()["access_token"]

    # Send attached token from user
    response = await client.get(
        "/auth/me", headers={"Authorization": f"Bearer {token}"}
    )
    # Check for status 200 OK
    assert response.status_code == 200
    # Ensure correct email is returned
    assert response.json()["email"] == "johndoe@example.com"


@pytest.mark.asyncio
async def test_unauthorized_access(client):
    # Attempt to hit protected route without token
    response = await client.get("/auth/me")
    # Check for status 401 Unauthorized
    assert response.status_code == 401
