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
async def test_create_unlinked_note(authorized_client):
    # Create note
    response = await authorized_client.post(
        "/notes/", json={"content": "This is a test note."}
    )
    # Check for status 201 Created
    assert response.status_code == 201
    # Parse the JSON response from server
    data = response.json()

    # Check if the response contains the correct note information
    assert data["content"] == "This is a test note."
    assert data["event_id"] is None
    assert "note_id" in data


@pytest.mark.asyncio
async def test_create_linked_note(authorized_client):
    # Create event
    event_response = await authorized_client.post(
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
    event_id = event_response.json()["event_id"]

    # Create note linked to the event
    note_response = await authorized_client.post(
        "/notes/",
        json={"content": "This is a note linked to an event.", "event_id": event_id},
    )
    # Check for status 201 Created
    assert note_response.status_code == 201
    # Check if note is linked to the correct event
    assert note_response.json()["event_id"] == event_id


@pytest.mark.asyncio
async def test_notes_list(authorized_client):
    # Create notes
    await authorized_client.post(
        "/notes/", json={"content": "First note for listing test."}
    )
    await authorized_client.post(
        "/notes/", json={"content": "Second note for listing test."}
    )
    await authorized_client.post(
        "/notes/", json={"content": "Third note for listing test."}
    )
    # List notes
    response = await authorized_client.get("/notes/")
    # Check for status 200 OK
    assert response.status_code == 200

    # Check if the response contains a list of notes, with correct size
    notes = response.json()
    assert len(notes) == 3

    # Check if the notes in the response contain the correct content
    contents = [note["content"] for note in notes]
    assert "First note for listing test." in contents
    assert "Second note for listing test." in contents
    assert "Third note for listing test." in contents


@pytest.mark.asyncio
async def test_update_note(authorized_client):
    # Create note
    create_response = await authorized_client.post(
        "/notes/", json={"content": "Note to be updated."}
    )
    # Extract note_id
    note_id = create_response.json()["note_id"]
    # Update the note's content
    update_response = await authorized_client.patch(
        f"/notes/{note_id}", json={"content": "Updated note content."}
    )
    # Check for status 200 OK
    assert update_response.status_code == 200
    # Check if the note's content was updated correctly
    assert update_response.json()["content"] == "Updated note content."


@pytest.mark.asyncio
async def test_delete_note(authorized_client):
    # Create note
    create_response = await authorized_client.post(
        "/notes/", json={"content": "Note to be deleted."}
    )
    # Extract note_id
    note_id = create_response.json()["note_id"]
    # Delete the note
    delete_response = await authorized_client.delete(f"/notes/{note_id}")
    # Check for status 204 No Content
    assert delete_response.status_code == 204


@pytest.mark.asyncio
async def test_attempt_to_relink_note(authorized_client):
    # Create first event
    event1_response = await authorized_client.post(
        "/events/",
        json={
            "title": "First Event",
            "description": "First Description",
            "location": "First Location",
            "start_time": "2026-07-01T10:00:00Z",
            "end_time": "2026-07-01T11:00:00Z",
            "category": "Other",
            "recurring": False,
        },
    )
    # Create second event
    event2_response = await authorized_client.post(
        "/events/",
        json={
            "title": "Second Event",
            "description": "Second Description",
            "location": "Second Location",
            "start_time": "2026-07-02T10:00:00Z",
            "end_time": "2026-07-02T11:00:00Z",
            "category": "Other",
            "recurring": False,
        },
    )
    # Extract event IDs
    event1_id = event1_response.json()["event_id"]
    event2_id = event2_response.json()["event_id"]
    # Create note linked to the first event
    note_response = await authorized_client.post(
        "/notes/",
        json={"content": "Note linked to first event.", "event_id": event1_id},
    )
    # Extract note_id
    note_id = note_response.json()["note_id"]

    # Attempt to update the note to link it to the second event
    update_response = await authorized_client.patch(
        f"/notes/{note_id}", json={"event_id": event2_id}
    )
    # Check for status 400 Bad Request
    assert update_response.status_code == 400
    assert update_response.json()["detail"] == "Note is already linked to another event"
