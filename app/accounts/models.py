import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.TextChoices):
    ADMIN = "admin", "Admin"
    OFFICE_MANAGER = "office_manager", "Office Manager"
    READONLY = "readonly", "Read-only"


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=32, choices=Role.choices, default=Role.READONLY)

    def is_admin(self) -> bool:
        return self.role == Role.ADMIN

    def is_office_manager(self) -> bool:
        return self.role == Role.OFFICE_MANAGER

    def is_readonly(self) -> bool:
        return self.role == Role.READONLY
