# Backup and restore

## Backup
- Postgres: `pg_dump` from `db` container
- Media: archive Docker volume `media_data`

## Restore
- Restore DB via `psql`
- Restore media files into `/app/media`
