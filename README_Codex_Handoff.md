# README_Codex_Handoff.md

## What this package is

This folder contains a Codex-ready planning package for a business-card archive MVP.

Files:
- `PRODUCT_SPEC.md` — product requirements
- `ARCHITECTURE.md` — implementation architecture and stack
- `AGENTS.md` — strict repo instructions for Codex
- `IMPLEMENTATION_PLAN.md` — phased execution plan
- `ACCEPTANCE_CRITERIA.md` — pass/fail conditions
- `TASKLIST.md` — granular task backlog
- `MASTER_PROMPT.md` — starter prompt for Codex

## How to use it

1. Create a new repository.
2. Copy these files into the repository root.
3. Start Codex in that repository.
4. Use the content of `MASTER_PROMPT.md` as the first task.
5. If you later add the real legacy DB schema or sample dump, ask Codex to implement the real import adapter on top of the existing generic import framework.

## Important limitation

The package is sufficient to build the application and a generic import framework, but the exact legacy importer still requires the real source schema.
