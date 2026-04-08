from pathlib import Path

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandParser

from imports.adapters.sample import FixtureSampleAdapter
from imports.services import run_import


class Command(BaseCommand):
    help = "Import bundled sample legacy data"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("--fixture", type=str, required=True)
        parser.add_argument("--username", type=str, default="")

    def handle(self, *args, **options):
        fixture = Path(options["fixture"])
        adapter = FixtureSampleAdapter(fixture)
        user = None
        username = options["username"]
        if username:
            user = get_user_model().objects.get(username=username)
        job = run_import(adapter=adapter, started_by=user)
        self.stdout.write(self.style.SUCCESS(f"Import completed: {job.id}"))
