# Task Manager API

A REST API for task management built with FastAPI and PostgreSQL. This project is part of my portfolio — it covers the core patterns you find in most web applications: user registration, JWT authentication, and full CRUD operations with strict data isolation between users.

This is not my first project. It was built to complement the other work in my portfolio and demonstrate backend fundamentals in a clean, structured way.

## Tech stack

- Python + FastAPI
- PostgreSQL + SQLAlchemy
- JWT Authentication
- Docker + docker-compose
- pytest
- GitHub Actions (CI)

## Getting started

Requires Docker and Docker Compose.

```bash
git clone https://github.com/JoaquinGodoy11/task-manager-api.git
cd task-manager-api
cp .env.example .env
```

Edit `.env` with your values, then:

```bash
docker compose up --build
```

API runs at `http://localhost:8000`
Swagger docs at `http://localhost:8000/docs`

## Running tests

```bash
docker compose exec api pytest tests/ -v
```

## Endpoints

### Auth
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Register a new user |
| POST | `/auth/login` | Login and get a JWT token |

### Tasks
All endpoints require a valid JWT token.

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/tasks/` | List your tasks |
| POST | `/tasks/` | Create a task |
| PUT | `/tasks/{id}` | Update a task |
| DELETE | `/tasks/{id}` | Delete a task |

## Project structure
app/
├── core/        # config, database, security
├── models/      # database tables
├── schemas/     # request and response validation
├── services/    # business logic
└── routers/     # endpoints

## Notes

Tasks are soft deleted — they are never removed from the database, just marked as inactive. Each user can only access their own tasks.