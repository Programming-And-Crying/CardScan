# TASKLIST.md

## Epic A — Foundations
- [ ] Initialize Django project and repository layout
- [ ] Add Docker Compose services: web, db, redis, worker, nginx
- [ ] Add Makefile and `.env.example`
- [ ] Configure Ruff, Black, mypy, pytest, Playwright
- [ ] Add health endpoints

## Epic B — Identity and access
- [ ] Implement custom user model/profile with roles
- [ ] Implement login/logout views and templates
- [ ] Implement role guards
- [ ] Implement AccessGroup model and admin/product UI
- [ ] Implement queryset/service helpers for group visibility
- [ ] Add tests for role and group behavior

## Epic C — Core domain
- [ ] Implement Contact model
- [ ] Implement alias/phone/email/website/address child models
- [ ] Implement BusinessCard model
- [ ] Implement ParsedField model
- [ ] Implement Comment model
- [ ] Implement ChangeHistory model
- [ ] Implement ProcessingTask model
- [ ] Implement ImportJob and ImportJobRow models
- [ ] Create factories and migrations

## Epic D — Browsing UI
- [ ] Dashboard page
- [ ] Contacts list page
- [ ] Contact detail page
- [ ] Card detail page
- [ ] Responsive layout shell

## Epic E — Editing flows
- [ ] Create contact form
- [ ] Edit contact form
- [ ] Card review/edit form
- [ ] Contact comments UI
- [ ] Card comments UI
- [ ] History views
- [ ] Delete flows for admin only

## Epic F — Upload and media
- [ ] Upload page and form
- [ ] File validation
- [ ] Local media storage integration
- [ ] Thumbnail generation
- [ ] Mobile-friendly capture input
- [ ] Post-upload card review entry point

## Epic G — Search
- [ ] Enable PostgreSQL extensions
- [ ] Create normalized and transliterated search fields
- [ ] Implement search service with ranking
- [ ] Add search form and result page
- [ ] Add tests for names/company/phone/email/raw text/transliteration

## Epic H — Review operations
- [ ] Implement needs-review queue
- [ ] Implement Human Verified flag and actions
- [ ] Add filters for verification and failures
- [ ] Add review workflow tests

## Epic I — OCR and processing
- [ ] Configure Celery and Redis integration
- [ ] Implement OCR task pipeline
- [ ] Integrate Tesseract
- [ ] Implement language detection best effort
- [ ] Implement field extraction heuristics
- [ ] Ensure manual values are preserved on reprocess
- [ ] Add processing status UI and tests

## Epic J — Historical import
- [ ] Define adapter protocol/ABC
- [ ] Implement generic import orchestration
- [ ] Implement fixture-backed sample adapter
- [ ] Add bundled sample data
- [ ] Add import command and/or admin trigger
- [ ] Add import reporting UI
- [ ] Write adapter extension docs for the real legacy source

## Epic K — Operational polish
- [ ] Product UI for user management
- [ ] Product UI for group management
- [ ] Product UI for imports and tasks
- [ ] Friendly error pages
- [ ] Backup/restore docs
- [ ] Seed/demo data command

## Epic L — Stabilization
- [ ] Fill acceptance-criteria gaps
- [ ] Add Playwright smoke tests
- [ ] Verify mobile layout on small viewport
- [ ] Final README pass
- [ ] Final docs pass
