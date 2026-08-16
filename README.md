# LifeEasy

## Overview

LifeEasy is an AI-powered personal assistant platform built with Python and FastAPI.

The goal of the project is to build a scalable backend capable of supporting multiple communication channels such as Telegram, WhatsApp, Viber, and Web.

This project is also my portfolio, where I demonstrate backend development, software architecture, authentication and authorization, automated testing, and DevOps practices.

---

## Current Features

### Authentication & Authorization

- JWT-based authentication
- Password hashing and verification
- Current authenticated user endpoint
- Role-based access control (RBAC)
- USER, ADMIN, and ROOT roles
- Protected API endpoints

### User Management

- User creation
- User listing with permission control
- User role management
- ROOT and ADMIN authorization rules

### Notes

- Create personal notes
- Get authenticated user's notes
- Get a single note by ID
- Update personal notes
- Delete personal notes
- Ownership-based access control
- ROOT can view all notes
- Users cannot access notes owned by other users

### Backend & Database

- FastAPI REST API
- PostgreSQL
- SQLAlchemy Async ORM
- Alembic database migrations
- Repository Pattern
- Service Layer
- Pydantic schemas
- Docker Compose

### Testing & Development

- Automated tests with Pytest
- Ruff code quality checks
- Feature branch workflow
- GitHub Pull Request workflow

---

## Architecture

LifeEasy follows a layered backend architecture:

```text
HTTP Request
     |
     v
API Layer
     |
     v
Service Layer
     |
     v
Repository Layer
     |
     v
PostgreSQL
```

Each layer has a separate responsibility:

- **API Layer** — handles HTTP requests, responses, dependencies, and status codes.
- **Service Layer** — contains business logic, permissions, and ownership rules.
- **Repository Layer** — handles database operations.
- **PostgreSQL** — stores persistent application data.

---

## Notes Access Control

| Action | USER | ADMIN | ROOT |
|---|---|---|---|
| Create own note | Yes | Yes | Yes |
| View own notes | Yes | Yes | Yes |
| Update own note | Yes | Yes | Yes |
| Delete own note | Yes | Yes | Yes |
| View another user's note | No | No | Yes |
| View all notes | No | No | Yes |

---

## Technology Stack

- Python 3.11.5
- FastAPI
- Pydantic
- SQLAlchemy
- PostgreSQL
- Alembic
- Docker
- Docker Compose
- Pytest
- Ruff
- JWT Authentication
- Git
- GitHub
- GitHub Actions (planned)

---

## Project Structure

```text
app/
├── api/
├── core/
├── db/
├── models/
├── repositories/
├── schemas/
├── services/

tests/
alembic/
```

---

## Roadmap

- Reminder service
- AI assistant
- WhatsApp integration
- Telegram integration
- Redis
- MongoDB
- CI/CD pipeline
- Docker production deployment
- Kubernetes

---

## Development Workflow

```text
feature branch
→ implementation
→ automated tests
→ Ruff checks
→ Pull Request
→ code review
→ merge
```

---

## Author

Backend & DevOps Portfolio Project by Vasyl Radashev.