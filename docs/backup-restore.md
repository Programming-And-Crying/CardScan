# Backup and restore

## Database backup
Use `pg_dump` against the running postgres service.

## Media backup
Backup docker volume `media_data` or the bind-mounted media directory.

## Restore
1. Restore Postgres dump.
2. Restore media files.
3. Run migrations.
