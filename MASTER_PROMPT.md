# MASTER_PROMPT.md

Read and follow these files before making changes:
- `AGENTS.md`
- `PRODUCT_SPEC.md`
- `ARCHITECTURE.md`
- `IMPLEMENTATION_PLAN.md`
- `ACCEPTANCE_CRITERIA.md`
- `TASKLIST.md`

Your job is to build the MVP described in those documents inside this repository.

## Required behavior
1. Scaffold the repository and application from scratch if needed.
2. Follow the exact stack and architecture in `ARCHITECTURE.md`.
3. Implement the work in the order defined by `IMPLEMENTATION_PLAN.md`.
4. Keep the app runnable at the end of each phase.
5. Add tests as you go.
6. Update docs as you go.
7. Do not silently skip requirements.
8. Do not invent the real legacy database schema.

## Special instruction for the legacy import
The real historical database schema is not present yet.
Implement:
- the generic pluggable import framework;
- a working fixture-based sample adapter;
- a documented placeholder for the real adapter.

Do not claim the real legacy adapter is complete unless the real schema/fixtures are present.

## Working mode
Proceed phase by phase:
- Phase 0
- Phase 1
- Phase 2
- ...
- Phase 12

At the end of each phase:
- run relevant tests;
- fix failures;
- update docs;
- summarize what is complete, what remains, and any blockers.

## Implementation priorities
Highest priority features:
- auth and roles
- access groups
- contacts and cards
- upload
- search
- comments and history
- review queue and Human Verified
- OCR processing pipeline
- generic import framework

## Non-goals
Do not add:
- React/Next.js frontend
- separate search engine
- cloud storage
- CRM integrations
- automatic duplicate merge
- full translation pipeline

## Quality bar
The final repo must be something a human engineer can run locally from a fresh clone, explore through the UI, test, and extend.
