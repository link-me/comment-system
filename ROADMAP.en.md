# ROADMAP (EN)

## Goals
- Basic CRUD for comments
- Moderation flag
- Simple file-based storage, no external services

## Done
- Express server
- CRUD endpoints
- Input validation
- Request logging (morgan)
- Docs and examples

## Planned
- Pagination in `GET /comments`
- `parentId` for threads
- Data export/import
- Storage: move to SQLite/PG if needed
- Dockerfile and compose

## Milestones
- v0.1 — MVP API with file store
- v0.2 — Pagination and threads
- v0.3 — Migrate storage to SQL