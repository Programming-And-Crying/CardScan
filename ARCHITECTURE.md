# ARCHITECTURE.md

## 1. Implementation approach

Build the MVP as a **single-repository Django monolith** with background workers and local file storage.

This is intentional.
The product needs:
- strong auth and permissions;
- admin workflows;
- forms and review pages;
- history and audit;
- local deployment;
- background OCR jobs;
- low operational complexity.

A Django-first architecture is the fastest way to get a maintainable working system with fewer moving parts than a separate SPA + API stack.

---

## 2. Required technology stack

Use exactly this stack unless a blocking technical reason is documented in the PR/summary:

### Backend
- Python 3.12
- Django 5.x
- Django templates for server-rendered UI
- HTMX for progressive enhancement where useful
- Django ORM

### Database
- PostgreSQL 16+
- `pg_trgm` extension
- `unaccent` extension

### Background processing
- Celery
- Redis

### OCR / text processing
- Tesseract OCR via system package and Python wrapper/subprocess
- `langdetect` or equivalent lightweight language detection library as best-effort only
- `Unidecode` for baseline transliteration fallback

### Frontend styling
- Tailwind CSS
- Minimal vanilla JS or Alpine.js only if needed

### File/image handling
- Pillow
- Local filesystem storage for originals and thumbnails

### Web server / deployment
- Docker Compose for local development and production-like local deployment
- Nginx as reverse proxy

### Testing and quality
- pytest
- pytest-django
- factory_boy
- Ruff
- Black
- mypy for core modules where practical
- Playwright for a small set of end-to-end smoke tests

Do not introduce React, Next.js, microservices, Elasticsearch, or object storage unless explicitly requested later.

---

## 3. System components

## 3.1 Django web app
Responsibilities:
- authentication;
- authorization;
- page rendering;
- forms and validation;
- admin UI;
- upload endpoints;
- business logic orchestration;
- audit log creation;
- review workflows.

## 3.2 PostgreSQL
Responsibilities:
- source of truth for domain data;
- permission-related joins;
- transactional integrity;
- full-text and trigram-assisted search.

## 3.3 Redis + Celery workers
Responsibilities:
- OCR tasks;
- thumbnail generation;
- normalization/transliteration tasks;
- import tasks;
- search document refresh tasks;
- retry of failed processing jobs.

## 3.4 Local media storage
Responsibilities:
- original scans;
- thumbnails;
- optional intermediate OCR artifacts.

Recommended directory layout inside container/host volume:
- `/app/media/originals/`
- `/app/media/thumbnails/`
- `/app/media/imports/`
- `/app/media/tmp/`

## 3.5 Nginx
Responsibilities:
- reverse proxy;
- serve static assets;
- serve media files in local deployment;
- TLS termination in deployment profile if needed.

---

## 4. Domain model

## 4.1 User
Use Django auth as base.
Extend user model with:
- role (`admin`, `office_manager`, `readonly`)
- active flag
- last_login metadata

## 4.2 AccessGroup
Fields:
- name
- slug
- description
- is_active
- created_at
- updated_at

## 4.3 Contact
Fields:
- full_name
- first_name
- last_name
- middle_name
- company
- position
- notes
- normalized_text
- transliterated_text
- search_document
- created_by
- updated_by
- created_at
- updated_at

Relationships:
- many-to-many with AccessGroup
- one-to-many aliases
- one-to-many phones
- one-to-many emails
- one-to-many websites
- one-to-many addresses
- one-to-many business cards
- one-to-many comments

## 4.4 ContactAlias
Fields:
- contact
- value
- source (`manual`, `xml`, `ocr`, `generated`)
- normalized_value
- transliterated_value

## 4.5 ContactPhone / ContactEmail / ContactWebsite / ContactAddress
Store each as separate normalized child table for easy querying and history tracking.

## 4.6 BusinessCard
Fields:
- contact (nullable while unresolved)
- original_file
- thumbnail_file
- source_type (`upload`, `legacy_import`)
- legacy_external_id
- language_code
- language_confidence
- xml_raw
- ocr_raw
- ocr_confidence
- parsed_text
- normalized_text
- transliterated_text
- processing_status (`uploaded`, `queued`, `processing`, `processed`, `needs_review`, `failed`)
- needs_manual_review
- human_verified
- verified_by
- verified_at
- created_by
- updated_by
- created_at
- updated_at

## 4.7 ParsedField
Purpose:
Store field-level provenance and confidence.

Fields:
- target_type (`contact`, `business_card`)
- target_id
- field_name
- field_value
- field_source (`manual`, `xml`, `ocr`, `generated`)
- confidence
- created_at
- updated_at
- updated_by

## 4.8 Comment
Fields:
- target_type
- target_id
- text
- created_by
- created_at
- updated_at
- is_deleted_soft

## 4.9 ChangeHistory
Fields:
- target_type
- target_id
- action_type
- field_name
- old_value_json
- new_value_json
- actor
- created_at

## 4.10 ProcessingTask
Fields:
- task_type
- target_type
- target_id
- status
- attempts
- started_at
- finished_at
- error_message
- metadata_json

## 4.11 ImportJob and ImportJobRow
Purpose:
Track imports and row-level outcomes.

---

## 5. Search design

Do **not** add a separate search engine for MVP.
Use PostgreSQL search features.

## 5.1 Searchable fields
Index and query across:
- contact full name and name parts;
- aliases;
- company;
- position;
- phones;
- emails;
- websites;
- addresses;
- notes;
- card OCR text;
- card XML-derived text;
- normalized text;
- transliterated text.

## 5.2 Search strategy
Implement a hybrid search approach:
1. exact filters for phone/email;
2. trigram similarity for names/company/position;
3. full-text search vector for broad text matches;
4. ranking layer that boosts structured exact matches above OCR text matches.

## 5.3 Search document refresh
Every mutation that changes searchable data must enqueue a search refresh task for the related Contact.

## 5.4 Access filtering
Search results must be filtered by access groups before rendering.
This rule must be enforced in server-side query logic, not only in templates.

---

## 6. OCR and text-processing pipeline

## 6.1 Trigger points
Create processing tasks when:
- a new card is uploaded;
- an imported card lacks good XML-derived fields;
- admin requests reprocess.

## 6.2 Processing steps
For each BusinessCard:
1. validate file and create thumbnail;
2. run OCR;
3. store raw OCR text;
4. run best-effort language detection on OCR text;
5. parse XML if available;
6. normalize extracted text;
7. generate transliterated search form;
8. extract candidate structured fields via heuristics;
9. mark `needs_manual_review` if key fields are missing or confidence is low;
10. refresh related Contact search document.

## 6.3 Field extraction heuristics
Implement pragmatic heuristics for MVP:
- email regex;
- phone normalization and regex;
- URL regex;
- simple line-based candidate extraction for company/name/position;
- XML field mapping when defined.

Do not build a heavy ML extraction service for MVP.

## 6.4 Human override
Manual edits always win.
Never overwrite a manual value with later OCR/XML processing.

---

## 7. Historical import design

## 7.1 Import principle
Because the real legacy schema is unknown at repository creation time, the codebase must provide a **pluggable adapter architecture**.

## 7.2 Adapter contract
Implement a clear Python protocol or abstract base class for adapters.
An adapter must expose something like:
- `iter_records()`
- each record includes external id, raw XML, image blob or file path, and optional pre-parsed fields.

## 7.3 Import pipeline
The core import service must:
- accept adapter-provided records;
- persist raw source material;
- create or update Contact and BusinessCard entities;
- map available XML fields;
- create ImportJob and ImportJobRow entries;
- queue OCR fallback when needed;
- log errors without aborting the whole import.

## 7.4 Deliverables for unknown source schema
The repo must include:
- a generic importer service;
- one example fixture-based adapter that fully works;
- a placeholder module for the real legacy DB adapter with TODO markers and documentation.

Do not fake support for the real legacy DB without actual schema samples.

---

## 8. Authorization design

## 8.1 Role checks
Implement role checks in Python service/view layer, not only in templates.

## 8.2 Group checks
A record is visible if:
- user is admin; or
- Contact shares at least one AccessGroup with the user.

## 8.3 Mutation rules
- readonly: no mutations
- office_manager: create/update, no delete
- admin: full access

## 8.4 Admin area
The admin area in the product UI must be restricted to admin users.
Django admin may also be enabled but must not replace the product admin pages entirely.

---

## 9. UI architecture

Use server-rendered templates.
Use HTMX only for interaction slices that benefit from partial updates, such as:
- live search results;
- review queue filtering;
- comment add/edit forms;
- contact match suggestions after upload.

Required template areas:
- auth
- dashboard
- contacts
- cards
- upload
- review queue
- admin users
- admin groups
- admin imports
- admin tasks

Responsive behavior is mandatory.
Design mobile-first for the upload and card review pages.

---

## 10. File handling

## 10.1 Accepted formats
Support at least:
- jpg/jpeg
- png
- webp
- pdf as optional first-page rasterization if feasible in MVP

If PDF support materially complicates MVP, implement images first but keep file validation extensible.

## 10.2 Storage rules
- never overwrite original files;
- generate thumbnails separately;
- store deterministic file paths based on UUID/date structure;
- keep metadata in DB.

---

## 11. Audit and history

Implement history capture in the application service layer or model signals, but keep it deterministic and testable.

Mandatory history events:
- contact created/updated/deleted;
- card created/updated/deleted;
- comments created/updated/deleted;
- access groups changed;
- human_verified changed;
- link/unlink card to contact.

---

## 12. API and route guidance

Even though the product is server-rendered, structure code into explicit application services and keep views thin.

Suggested route map:
- `/login/`
- `/logout/`
- `/`
- `/contacts/`
- `/contacts/<uuid:pk>/`
- `/contacts/<uuid:pk>/edit/`
- `/cards/<uuid:pk>/`
- `/cards/<uuid:pk>/edit/`
- `/upload/`
- `/review-queue/`
- `/history/contact/<uuid:pk>/`
- `/history/card/<uuid:pk>/`
- `/admin-ui/users/`
- `/admin-ui/groups/`
- `/admin-ui/imports/`
- `/admin-ui/tasks/`
- `/health/live/`
- `/health/ready/`

Provide JSON endpoints only when needed by HTMX or tests.

---

## 13. Repository layout

Codex should create a repository roughly like this:

```text
.
├── AGENTS.md
├── README.md
├── PRODUCT_SPEC.md
├── ARCHITECTURE.md
├── IMPLEMENTATION_PLAN.md
├── ACCEPTANCE_CRITERIA.md
├── TASKLIST.md
├── MASTER_PROMPT.md
├── docker-compose.yml
├── Makefile
├── .env.example
├── docs/
│   ├── import-adapter.md
│   ├── deployment.md
│   ├── backup-restore.md
│   └── user-guides/
├── app/
│   ├── manage.py
│   ├── config/
│   ├── accounts/
│   ├── access/
│   ├── contacts/
│   ├── cards/
│   ├── search/
│   ├── comments/
│   ├── history/
│   ├── imports/
│   ├── processing/
│   ├── dashboard/
│   ├── templates/
│   └── static/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
└── fixtures/
    └── legacy_sample/
```

---

## 14. Required make targets

Codex must implement a Makefile with at least:
- `make init`
- `make dev`
- `make migrate`
- `make test`
- `make lint`
- `make format`
- `make worker`
- `make import-sample`
- `make e2e`

---

## 15. Required documentation output

The finished repository must include:
- setup instructions;
- environment variables documentation;
- deployment instructions for local network deployment;
- import adapter guide;
- backup/restore guide;
- role and permission documentation.
