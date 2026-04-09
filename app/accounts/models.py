from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRole(models.TextChoices):
    ADMIN = "admin", "Admin"
    OFFICE_MANAGER = "office_manager", "Office manager"
    READONLY = "readonly", "Read-only"


class User(AbstractUser):
    role = models.CharField(max_length=32, choices=UserRole.choices, default=UserRole.READONLY)
    access_groups = models.ManyToManyField("access.AccessGroup", blank=True, related_name="users")

    @property
    def can_delete(self) -> bool:
        return self.role == UserRole.ADMIN

    @property
    def can_edit(self) -> bool:
        return self.role in {UserRole.ADMIN, UserRole.OFFICE_MANAGER}
