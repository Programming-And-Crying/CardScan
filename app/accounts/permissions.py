from functools import wraps
from django.http import HttpRequest, HttpResponseForbidden

from accounts.models import UserRole


def role_required(*roles: str):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request: HttpRequest, *args, **kwargs):
            if not request.user.is_authenticated:
                return HttpResponseForbidden()
            if request.user.role not in roles:
                return HttpResponseForbidden()
            return view_func(request, *args, **kwargs)

        return _wrapped

    return decorator


def can_mutate(user) -> bool:
    return user.is_authenticated and user.role in {UserRole.ADMIN, UserRole.OFFICE_MANAGER}


def is_admin(user) -> bool:
    return user.is_authenticated and user.role == UserRole.ADMIN
