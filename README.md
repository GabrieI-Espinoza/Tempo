# Tempo

Tempo is a calendar-centered memory system designed to organize notes around time instead of folders, tags, or scattered documents.

The core idea is that a calendar should capture more than scheduled events. It should also preserve the thoughts, context, and decisions connected to those moments. Instead of treating notes and events as separate systems, Tempo connects them so time itself becomes the organizing structure.

## Product Vision

### Calendar as Memory Timeline
In Tempo, the calendar is more than a scheduling surface. It becomes a timeline of activity and thought, where each event can carry the notes, context, and reflections associated with that period of time.

### Context-Locked Notes
Notes are attached to moments, not buried in folders. Instead of asking “where did I save that?”, Tempo is built around the question “when was I thinking about this?”

### Color-Coded Structure
Events are organized by category and associated color metadata, creating a visual structure that helps users quickly distinguish different parts of their lives and workflows.

### TempoPad
TempoPad is the idea of a lightweight capture space for notes that do not yet belong to a specific event. These “orphan thoughts” can be written quickly first, then attached to a moment in time later.

## Server Features

- User registration and login
- JWT-based authentication
- Authenticated user profile retrieval
- CRUD operations for calendar events
- CRUD operations for notes
- Optional linking of notes to events
- Event categories with color values
- Per-user ownership enforcement for protected resources
- PostgreSQL integration with Tortoise ORM


## API Overview

### Auth
- `POST /auth/register`
- `POST /auth/login`
- `GET /auth/me`

### Categories
- `GET /categories/`

### Events
- `POST /events/`
- `GET /events/`
- `PATCH /events/{event_id}`
- `DELETE /events/{event_id}`

### Notes
- `POST /notes/`
- `GET /notes/`
- `GET /notes/?event_id={event_id}`
- `PATCH /notes/{note_id}`
- `DELETE /notes/{note_id}`

## Local Setup

### 1. Clone the repository
```bash
git clone https://github.com/GabrieI-Espinoza/Tempo.git
cd Tempo-main
```
### 2. Create environment variables
```bash
# Fill in required variables
cp .env.example .env
```
## 3. Start PostgreSQL
```bash
docker compose up -d
```
## 4. Set up the backend
```bash
cd server
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
## 5. Run server
```bash
fastapi dev app/main.py
```
