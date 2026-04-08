# CardScan MVP

CardScan is a local-network Django monolith for business-card archiving, review, and search.

## Current implementation status

This iteration delivers foundational vertical slices:
- Phase 0: repository scaffold, docker compose stack, Makefile, env config, health endpoints.
- Phase 1: authentication with role-aware custom user model and guarded edit path.
- Phase 2: access groups and visibility selector enforcement for contact list/detail.
- Phase 3 (partial): core models for contacts/cards/comments/history/tasks/import jobs.
- Phase 10 (partial): pluggable import framework and fixture-backed sample adapter.

## Quick start

1. Copy env:
   ```bash
   cp .env.example .env
   ```
2. Build containers:
   ```bash
   make init
   ```
3. Run migrations:
   ```bash
   make migrate
   ```
4. Start stack:
   ```bash
   make dev
   ```

App URL: `http://localhost:8000`

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

## Roles

- `admin`: full access including delete and system operations.
- `office_manager`: create/edit and verify; no delete.
- `readonly`: read/search only.

## Notes on legacy import

The real legacy DB schema is not present in this repo. A placeholder adapter is included and intentionally raises `NotImplementedError` until schema/fixtures are available.
