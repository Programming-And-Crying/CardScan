from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from access.models import AccessGroup


class Command(BaseCommand):
    help = "Seed demo users and groups"

    def handle(self, *args, **options):
        group, _ = AccessGroup.objects.get_or_create(name="Default", slug="default")
        User = get_user_model()
        for username, role in [("admin", "admin"), ("manager", "office_manager"), ("reader", "readonly")]:
            user, created = User.objects.get_or_create(username=username, defaults={"role": role, "is_staff": role == "admin", "is_superuser": role == "admin"})
            if created:
                user.set_password("password123")
                user.save()
                user.access_groups.add(group)
        self.stdout.write(self.style.SUCCESS("Seeded demo users (password123)."))
