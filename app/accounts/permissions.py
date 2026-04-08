from django.core.exceptions import PermissionDenied

from .models import Role, User


def require_admin(user: User) -> None:
    if user.role != Role.ADMIN:
        raise PermissionDenied("Admin role required")


def require_editor(user: User) -> None:
    if user.role == Role.READONLY:
        raise PermissionDenied("Read-only users cannot mutate records")
