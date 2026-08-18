# LifeEasy Architecture

LifeEasy is a scalable AI assistant platform with one intelligent core and multiple communication channels.

## Architecture Overview

The backend follows a layered architecture:

API → Service → Repository → Database

Each layer has a separate responsibility.

### API Layer

The API layer handles HTTP requests and responses.

Responsibilities:

- receive and validate requests
- authenticate users
- resolve the current user
- call the appropriate service
- return HTTP responses

Main API modules:

- authentication
- users
- notes
- reminders
- assistant
- health

### Service Layer

The service layer contains application and business logic.

Responsibilities:

- coordinate application operations
- enforce ownership rules
- raise domain-specific exceptions
- communicate with repositories

Examples:

- `NoteService`
- `ReminderService`

The service layer does not communicate directly with PostgreSQL.

### Repository Layer

The repository layer handles database operations.

Responsibilities:

- create records
- retrieve records
- update records
- delete records
- filter records by owner

Examples:

- `NoteRepository`
- `ReminderRepository`

Repositories use SQLAlchemy and asynchronous database sessions.

### Database Layer

PostgreSQL is used as the primary relational database.

SQLAlchemy provides ORM and database access.

Alembic manages database schema migrations.

Current persistent entities include:

- users
- notes
- reminders

## Authentication

LifeEasy uses JWT-based authentication.

A protected request follows this flow:

Request
→ JWT token
→ `get_current_user`
→ authenticated User
→ Service
→ Repository
→ PostgreSQL

The client does not choose the resource owner manually.

For example, when a reminder is created, `owner_id` comes from the authenticated user.

## Ownership Protection

Notes and reminders belong to individual users.

Resources are protected using ownership checks.

Example:

User A → Reminder A → access allowed

User B → Reminder A → access denied

For protected individual resources, a resource that does not exist or does not belong to the current user results in a not-found error.

This prevents users from accessing or modifying another user's private resources.

## Notes

Notes support CRUD operations with ownership protection.

Supported operations:

- create a note
- list user's notes
- retrieve a note
- update a note
- delete a note

## Reminders

Reminders support CRUD operations with ownership protection.

Supported operations:

- `POST /reminders/`
- `GET /reminders/`
- `GET /reminders/{id}`
- `PATCH /reminders/{id}`
- `DELETE /reminders/{id}`

Reminder timestamps are timezone-aware.

Each reminder belongs to an authenticated user.

## Exception Handling

Domain-specific exceptions are handled globally.

Examples:

- `NoteNotFoundError`
- `ReminderNotFoundError`

The service layer raises domain exceptions, while FastAPI exception handlers convert them into HTTP responses.

This keeps HTTP-specific logic out of the service layer.

## Logging

Application logging is configured centrally.

API operations can produce structured application logs for debugging and monitoring.

## Testing

The project uses pytest for automated testing.

Tests cover:

- authentication
- authorization
- notes
- reminders
- ownership isolation
- CRUD operations

The current test suite contains 27 passing tests.

## Code Quality

Ruff is used for linting and formatting.

The project currently passes:

- pytest
- Ruff checks

## Current Request Flow

A typical request follows this path:

Client
→ FastAPI Router
→ Authentication
→ Service
→ Repository
→ SQLAlchemy
→ PostgreSQL

Response:

PostgreSQL
→ Repository
→ Service
→ API
→ Client

## Future Architecture

The reminder system currently stores and manages reminders.

The next architectural stage is reminder execution:

Reminder
→ scheduler
→ due reminder detection
→ execution
→ communication channel

Future communication channels may include:

- WhatsApp
- Telegram
- Viber

The core application should remain independent of a specific communication channel.