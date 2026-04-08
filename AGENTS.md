# AGENTS.md

## Mission
Build a production-oriented MVP of a local-network business-card archive system exactly as described in:
- `PRODUCT_SPEC.md`
- `ARCHITECTURE.md`
- `IMPLEMENTATION_PLAN.md`
- `ACCEPTANCE_CRITERIA.md`
- `TASKLIST.md`

This repository starts from planning documents.
You are expected to create the full application scaffold and implement the MVP in vertical slices.

---

## Hard constraints

1. Use the stack defined in `ARCHITECTURE.md`.
2. Keep the solution in a **single Django monorepo-style application**.
3. Prefer server-rendered templates with HTMX over a separate SPA.
4. Use PostgreSQL search capabilities; do not add Elasticsearch/OpenSearch/Meilisearch.
5. Use local filesystem storage for media.
6. Use Celery + Redis for background processing.
7. Preserve raw XML and raw OCR text.
8. Manual edits always take precedence over XML and OCR.
9. Office manager must not get delete permissions.
10. Do not pretend the real legacy DB adapter is complete unless the real schema/fixtures exist in the repo.

---

## Delivery rules

1. Work in small, reviewable commits if a VCS workflow is available.
2. Implement the repository in vertical slices that always leave the app runnable.
3. Each slice must update tests and docs.
4. Do not leave dead code, placeholder TODOs without explanation, or silently skipped requirements.
5. When a requirement is intentionally deferred because the planning docs mark it out of scope, document that choice explicitly.
6. Before changing architecture, verify whether the existing planning docs already answer the question.
7. Keep views thin and business logic in services/selectors where practical.
8. Avoid hidden magic. Favor explicit, readable code.
9. Favor maintainability over cleverness.
10. Favor deterministic tests over mocks when practical.

---

## Definition of done

A task is done only when all of the following are true:
- implementation exists;
- tests for the change exist and pass;
- lint/format checks pass;
- user-facing behavior is documented if relevant;
- acceptance criteria tied to the task are satisfied;
- no obvious placeholder stubs remain unless explicitly documented as blocked by missing external inputs.

---

## Required commands

The repository must support these commands:
- `make init`
- `make dev`
- `make migrate`
- `make test`
- `make lint`
- `make format`
- `make worker`
- `make import-sample`
- `make e2e`

If one of these commands is initially missing, create it.

---

## Required implementation order

Follow `IMPLEMENTATION_PLAN.md`.
Do not jump straight to OCR or import before the core auth/domain skeleton exists.
Recommended order:
1. repo scaffold and local dev environment
2. auth and roles
3. access groups
4. contacts and cards models
5. upload and media handling
6. search
7. comments and history
8. review queue and human verification
9. processing worker and OCR pipeline
10. import framework and sample adapter
11. admin UI and operational polish
12. end-to-end stabilization

---

## Search requirements

Search is core product value.
Do not ship a weak placeholder search that only does `icontains` on one field.
The MVP must search across structured fields and broad text using PostgreSQL features described in `ARCHITECTURE.md`.

---

## Import requirements

There is one known external blocker: the real historical database schema is not yet in the repository.
Therefore:
- implement the generic import framework;
- implement a working sample adapter using bundled fixtures;
- document how the real adapter should be added;
- do not invent unsupported assumptions about the legacy schema.

---

## OCR requirements

OCR is required for MVP but should remain pragmatic.
Use Tesseract plus lightweight heuristics.
Do not introduce an external AI extraction service.
Do not attempt semantic translation.
Manual correction UI is mandatory.

---

## Security requirements

Always enforce permissions server-side.
Never trust hidden buttons or client-side checks.
Views, forms, services, and querysets must all respect role and group restrictions.

---

## Testing requirements

Minimum required test coverage areas:
- auth and permission gates
- group-based visibility filtering
- contact/card creation and editing
- upload flow
- history creation
- comments
- search behavior
- human verification flow
- import sample adapter
- OCR task orchestration with mocked OCR execution where needed

Keep unit and integration tests balanced.
Add a few Playwright smoke tests for key flows.

---

## Documentation requirements

Whenever you add or change developer workflow, update:
- `README.md`
- docs under `docs/`
- planning docs if the contract changed

Do not let documentation drift.

---

## When blocked

If blocked by missing external inputs:
1. implement everything that can be completed without the missing input;
2. isolate the blocked part behind a clear interface;
3. document the blocker in code and docs;
4. do not claim the blocked part is production-ready.

---

## Preferred coding style

- explicit types where useful
- small focused modules
- service functions or classes for side-effect-heavy workflows
- selectors/query helpers for complex queryset logic
- forms for validation of web mutations
- clean templates with minimal business logic
- UUID primary keys for main business entities

---

## Final repository expectation

The repository should be something a human engineer can:
- clone;
- configure from `.env.example`;
- start with Docker Compose;
- migrate;
- seed with sample data;
- run tests;
- hand over for further development.
