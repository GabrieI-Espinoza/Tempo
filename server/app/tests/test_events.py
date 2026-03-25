import pytest
import pytest_asyncio


@pytest_asyncio.fixture
async def authorized_client(client):
    # Register user
    response = await client.post(
        "/auth/register",
        json={
            "email": "johndoe@example.com",
            "password": "strongpassword123",
            "first_name": "John",
            "last_name": "Doe",
        },
    )
    # Extract token
    token = response.json()["access_token"]

    # Attach token to client headers, to mimic an authenticated user making requests
    client.headers["Authorization"] = f"Bearer {token}"
    # Return the client with the attached token for use in tests
    return client


@pytest.mark.asyncio
async def test_create_event(authorized_client):
    # Create event
    response = await authorized_client.post(
        "/events/",
        json={
            "title": "Test Event",
            "description": "Test Description",
            "location": "Test Location",
            "start_time": "2026-07-01T10:00:00Z",
            "end_time": "2026-07-01T11:00:00Z",
            "category": "Other",
            "recurring": False,
        },
    )
    # Check for status 201 Created
    assert response.status_code == 201
    # Check if the response contains the correct event information
    assert response.json()["title"] == "Test Event"
    assert response.json()["description"] == "Test Description"
    assert response.json()["location"] == "Test Location"
    assert response.json()["start_time"] == "2026-07-01T10:00:00Z"
    assert response.json()["end_time"] == "2026-07-01T11:00:00Z"
    assert response.json()["category"] == "Other"
    assert response.json()["recurring"] == False


@pytest.mark.asyncio
async def test_create_invalid_event(authorized_client):
    # Attempt to create an event with invalid data
    response = await authorized_client.post(
        "/events/",
        json={
            "title": "Invalid Event",
            "description": "This event has an end time before the start time",
            "location": "Test Location",
            "start_time": "2026-07-01T11:00:00Z",
            "end_time": "2026-07-01T10:00:00Z",
            "category": "Other",
            "recurring": False,
        },
    )
    # Check for status 422 Unprocessable Content
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_list_events(authorized_client):
    # Create multiple events for the user
    await authorized_client.post(
        "/events/",
        json={
            "title": "Event 1",
            "description": "Test Description 1",
            "location": "Test Location 1",
            "start_time": "2026-03-25T10:00:00Z",
            "end_time": "2026-03-25T11:00:00Z",
        },
    )
    await authorized_client.post(
        "/events/",
        json={
            "title": "Event 2",
            "description": "Test Description 2",
            "location": "Test Location 2",
            "start_time": "2026-03-26T10:00:00Z",
            "end_time": "2026-03-26T11:00:00Z",
        },
    )
    await authorized_client.post(
        "/events/",
        json={
            "title": "Event 3",
            "description": "Test Description 3",
            "location": "Test Location 3",
            "start_time": "2026-03-27T10:00:00Z",
            "end_time": "2026-03-27T11:00:00Z",
        },
    )
    # Get list of events for the user
    response = await authorized_client.get("/events/")
    # Check for status 200 OK
    assert response.status_code == 200
    # Check that the response contains the correct number of events
    events = response.json()
    assert len(events) == 3


@pytest.mark.asyncio
async def test_update_event(authorized_client):
    # Create event
    create_response = await authorized_client.post(
        "/events/",
        json={
            "title": "Original Event",
            "description": "Original Description",
            "location": "Original Location",
            "start_time": "2026-04-01T10:00:00Z",
            "end_time": "2026-04-01T11:00:00Z",
        },
    )
    # Extract event_id
    event_id = create_response.json()["event_id"]
    # Update the event with new data
    update_response = await authorized_client.patch(
        f"/events/{event_id}",
        json={
            "title": "Updated Event",
            "description": "Updated Description",
            "location": "Updated Location",
        },
    )
    # Check for status 200 OK
    assert update_response.status_code == 200
    # Check if the response contains the updated event information
    assert update_response.json()["title"] == "Updated Event"
    assert update_response.json()["description"] == "Updated Description"
    assert update_response.json()["location"] == "Updated Location"


@pytest.mark.asyncio
async def test_delete_event(authorized_client):
    # Create event
    create_response = await authorized_client.post(
        "/events/",
        json={
            "title": "Event to Delete",
            "start_time": "2026-05-01T10:00:00Z",
            "end_time": "2026-05-01T11:00:00Z",
        },
    )
    event_id = create_response.json()["event_id"]

    # Delete event
    delete_response = await authorized_client.delete(f"/events/{event_id}")
    assert delete_response.status_code == 204

    # Verify it is gone from the list
    get_response = await authorized_client.get("/events/")
    assert get_response.status_code == 200
    assert all(event["event_id"] != event_id for event in get_response.json())
