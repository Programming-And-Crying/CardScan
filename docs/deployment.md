# Local deployment

This MVP is designed for local-network deployment with Docker Compose:
- Postgres 16
- Redis
- Django web app
- Celery worker
- Nginx reverse proxy

Media is stored on local docker volume mounted at `/app/app/media`.
