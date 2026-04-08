# IMPLEMENTATION_PLAN.md

## Phase 0 — Repository bootstrap

### Goal
Create the project skeleton and reproducible local environment.

### Deliverables
- Django project scaffold
- Docker Compose with web, db, redis, worker, nginx
- Makefile
- `.env.example`
- base README
- pytest, Ruff, Black, mypy, Playwright configuration

### Done when
- `make init` works from a fresh clone
- `make dev` starts the application stack
- health endpoints respond
- CI-style local test/lint commands exist

---

## Phase 1 — Authentication and role model

### Goal
Implement login/logout, user model extension, and role gates.

### Deliverables
- custom user model or profile model with role field
- login page
- logout action
- authenticated dashboard
- role decorators/mixins/helpers
- tests for access denial/approval

### Done when
- admin, office manager, readonly users can sign in
- unauthorized users cannot access protected pages
- readonly users cannot mutate data

---

## Phase 2 — Access groups and visibility enforcement

### Goal
Implement group-based record visibility.

### Deliverables
- AccessGroup model
- user-group assignment
- contact-group assignment
- selectors/query helpers enforcing visibility
- admin UI for groups
- tests for visibility intersections

### Done when
- non-admin users only see records in intersecting groups
- admin sees all records

---

## Phase 3 — Core domain models

### Goal
Implement Contact, BusinessCard, aliases, structured child records, comments, history skeleton.

### Deliverables
- Contact-related models
- BusinessCard model
- child models for phones/emails/etc.
- UUID primary keys
- migrations
- admin registration for debugging
- factories and basic tests

### Done when
- core records can be created in DB
- relations behave correctly

---

## Phase 4 — Contact and card UI

### Goal
Implement primary pages for browsing and viewing records.

### Deliverables
- dashboard
- contacts list page
- contact detail page
- card detail page
- responsive templates

### Done when
- readonly user can browse allowed contacts and cards
- pages render correctly on small viewport widths

---

## Phase 5 — Edit flows, comments, and history

### Goal
Implement create/edit flows and auditability.

### Deliverables
- create/edit contact pages
- create/edit card review forms
- comments on contact/card
- change history capture
- history views

### Done when
- office manager can edit allowed records
- admin can delete
- readonly cannot mutate
- history entries are created for key mutations

---

## Phase 6 — Upload and media pipeline

### Goal
Implement file upload and thumbnail creation.

### Deliverables
- upload page
- server-side file validation
- local file storage integration
- thumbnail generation task
- mobile-friendly camera/file input
- status feedback after upload

### Done when
- office manager can upload one image card at a time
- original and thumbnail are stored
- uploaded card appears in review flow

---

## Phase 7 — Search

### Goal
Implement useful search over structured and raw text.

### Deliverables
- normalized/transliterated search fields
- PostgreSQL trigram and FTS setup
- search service/selectors
- ranked results page
- tests covering exact and fuzzy scenarios

### Done when
- search works across name/company/position/phone/email/text
- results respect access groups

---

## Phase 8 — Human verification and review queue

### Goal
Implement operational review workflows.

### Deliverables
- review queue page
- filters for needs review / not verified / failed processing
- human_verified action
- history entries for verification state

### Done when
- office manager can process queue items and mark verified

---

## Phase 9 — OCR and text processing worker

### Goal
Implement OCR, normalization, transliteration, and field extraction.

### Deliverables
- Celery tasks for OCR pipeline
- Tesseract integration
- best-effort language detection
- extraction heuristics
- fallback handling and retries
- tests around task orchestration

### Done when
- a new uploaded card is processed in background
- OCR text and extracted values are visible in the UI
- manual values are never overwritten

---

## Phase 10 — Import framework and sample legacy adapter

### Goal
Implement pluggable import architecture.

### Deliverables
- adapter protocol / abstract base class
- core import service
- sample fixture adapter
- ImportJob / ImportJobRow models and UI
- `make import-sample`
- documentation for real adapter integration

### Done when
- bundled sample data can be imported successfully
- import report shows successes/failures

---

## Phase 11 — Admin and operational polish

### Goal
Implement the missing operational pages and safeguards.

### Deliverables
- user management UI
- task monitoring UI
- import management UI
- basic system status page
- friendly error pages
- backup/restore documentation

### Done when
- admin can manage users/groups/imports from product UI

---

## Phase 12 — Stabilization and acceptance pass

### Goal
Close gaps against acceptance criteria.

### Deliverables
- acceptance checklist completed
- test stabilization
- documentation pass
- example seed data
- final README

### Done when
- repository satisfies `ACCEPTANCE_CRITERIA.md`
- smoke tests pass
- setup from clean clone is documented and verified
