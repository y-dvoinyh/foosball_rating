# Project Instructions

## Project Stack

- Backend: FastAPI, Pydantic v2, SQLAlchemy 2 async, Alembic.
- Database: PostgreSQL.
- Background jobs: Redis, Celery worker, Celery Beat.
- Frontend: Vue 3, Quasar, TypeScript, Pinia, Vue Router, Axios.
- Reverse proxy and local entrypoint: nginx.
- Local development: Docker Compose, pgAdmin, bind mounts with hot reload.
- Documentation: MkDocs Material.
- Backend quality tools: pytest, Ruff lint/format.
- Frontend quality tools: Vitest, ESLint, Prettier, `vue-tsc`.
- CI: GitHub Actions.

## Local Services

- Main app through nginx: `http://localhost:8080`.
- Frontend dev server: `http://localhost:5173`.
- Backend API: `http://localhost:8000`.
- Backend API docs: `http://localhost:8000/docs`.
- PostgreSQL: `localhost:5432`.
- Redis: `localhost:6379`.
- pgAdmin: `http://localhost:5051`.
- DB migrations run through the one-shot `migrate` Docker Compose service before backend startup.

## Project Shape

- `frontend` contains the public UI and future admin panel.
- `backend` contains API, domain logic, auth, permissions, import, rating calculation, and background task integration.
- `docs` contains detailed project documentation; keep `AGENTS.md` as a compact operational summary for agents.
- Backend uses a feature-first modular monolith. Main modules: `auth`, `players`, `competitions`, `ratings`, `imports`.
- `competitions` owns leagues, seasons, competitions, teams, matches, and sets. Do not create separate top-level backend modules for each of those at the start.
- Live behavior is not a separate domain module at the start: external polling belongs to `imports`; recalculation and prepared snapshots belong to `ratings`.

## Git Workflow

- Use short task branches from `develop` when creating new work branches.
- Use branch prefixes from project docs: `feature/`, `fix/`, `hotfix/`, `chore/`, `docs/`, `refactor/`, `experiment/`, or `release/`.
- Never use the word `codex` in branch names.
- Prefer Conventional Commits, for example `feat(auth): add email confirmation` or `fix(rating): handle duplicate history rows`.
- Keep changes small and easy to review.

## Verification Policy

Do not run tests, linters, typecheck, Docker builds, or full verification automatically after every small edit.

Default workflow:

- For small edits, make the change and inspect the diff/status only.
- Run narrow tests only when the change is risky, changes behavior, or the user asks.
- Run full checks only before a commit or when the user explicitly asks with phrases like "проверь", "запусти тесты", or "полная проверка".
- Do not rebuild or restart Docker containers unless manual browser/API verification is needed or the user asks.
- For documentation-only changes, do not run tests unless requested.

Prefer small, easy-to-review iterations. Keep verification proportional to the risk and size of the change.

## Documentation

- Important architecture decisions belong in `docs/architecture/adr/`.
- Keep the root README short; detailed instructions belong in `docs/`.
- Update documentation in the same change when code changes behavior, architecture, or development process.

## Architecture Principles

- Keep backend domain boundaries coarse and practical: prefer `backend/app/modules/<domain>/` modules over scattered global `models`, `schemas`, and `services` for new domain code.
- Simple modules may stay flat with `models.py`, `schemas.py`, `repository.py`, `service.py`, `router.py`, and `tasks.py`; introduce `domain/`, `application/`, `infrastructure/`, and `presentation/` only when module complexity justifies it.
- Public pages should read prepared data and be optimized for read performance.
- Heavy operations, imports, and rating recalculations should run in background jobs, not in long HTTP requests.
- Imported source data should be preserved for debugging and reproducibility.
- Database schema changes must be represented as Alembic migrations.
- Auth is a modular monolith inside the backend for now, with a clear boundary so it can be extracted later.
- Other backend modules should use auth dependencies/service interfaces instead of parsing JWTs, touching refresh tokens, or reading auth internals directly.
- Rating calculation should have a pure core that does not depend on FastAPI, SQLAlchemy, Celery, or Redis; routers and tasks should call application services instead of containing rating or import business logic.
- The frontend public pages should be fast and comfortable for viewing.
- The admin panel should be a practical work tool, not a decorative page.
- Use Quasar components for tables, filters, and forms.

## Auth Contract

- Auth endpoints are `/auth/register`, `/auth/login`, `/auth/refresh`, `/auth/logout`, and `/auth/me`.
- Access tokens are short-lived JWTs passed as `Authorization: Bearer <access_token>`.
- The frontend stores the access token in memory only.
- Refresh tokens are stored in `HttpOnly`, `Secure`, `SameSite` cookies; local development may disable `Secure` for `http://localhost`.
- A separate non-secret cookie hint may be used so the frontend can skip refresh when there is clearly no session.
- Do not store access or refresh tokens in `localStorage`.

## Common Commands

- Start local stack: `docker compose up --build` or `make up`.
- Stop local stack: `make down`.
- Show logs: `make logs`.
- Run migrations: `docker compose up migrate` or `make migrate`.
- Create Alembic migration locally from `backend`: `alembic revision --autogenerate -m "migration name"`.
- Apply Alembic migrations locally from `backend`: `alembic upgrade head`.
- Backend tests through Docker: `docker compose run --rm backend-tests`.
- Frontend tests through Docker: `docker compose run --rm frontend-tests`.
- Backend lint through Docker: `docker compose run --rm backend-lint`.
- Frontend lint through Docker: `docker compose run --rm frontend-lint`.
- Frontend typecheck from `frontend`: `npm run typecheck`.
- Docs serve: `mkdocs serve` or `make docs`.
- Docs build: `mkdocs build` or `make docs-build`.
- Ensure local dev superuser: `make ensure-dev-superuser`.
