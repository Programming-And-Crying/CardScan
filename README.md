# CardScan MVP

Local-network Django monolith for business card archive/search/review.

## Stack
- Django 5 + server templates + HTMX
- PostgreSQL 16 (`pg_trgm`, `unaccent` migrations)
- Celery + Redis
- Tesseract OCR via `pytesseract`
- Local filesystem media storage
- Docker Compose + Nginx

## Quick start (clean clone)
1. Copy env file:
   ```bash
   cp .env.example .env
   ```
2. Build containers:
   ```bash
   make init
   ```
3. Start full stack:
   ```bash
   make dev
   ```
4. In another terminal, seed demo users:
   ```bash
   make seed
   ```
5. Optional sample import:
   ```bash
   make import-sample
   ```

App URL: `http://localhost:8000`

## Demo credentials
All seeded users use password `password123`:
- `admin` (role: `admin`)
- `manager` (role: `office_manager`)
- `reader` (role: `readonly`)

## Required commands
- `make init`
- `make dev`
- `make migrate`
- `make test`
- `make lint`
- `make format`
- `make worker`
- `make import-sample`
- `make e2e`

## Implemented MVP flows
- Login/logout and protected pages.
- Role permissions (`admin`, `office_manager`, `readonly`).
- Access-group visibility filtering for contacts/cards/search.
- Contacts list/detail/create/edit/delete (delete admin-only).
- Card upload + asynchronous OCR task enqueue + review queue.
- OCR/XML processing interfaces and persisted raw OCR/XML fields.
- Contact/card comments + comment edit metadata history.
- Change history records for key mutations.
- Human verified flag handling on card review form.
- Admin basics for user/group/import/task/system pages.

## Legacy import status
- Generic importer + sample fixture adapter implemented.
- Real legacy DB adapter remains intentionally blocked until real legacy schema/sample dump is available.

See docs in `docs/` for import adapter details, deployment notes, backup/restore, and roles.
