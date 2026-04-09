from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from imports.adapters import SampleFixtureAdapter
from imports.services import run_import


class Command(BaseCommand):
    help = "Run sample fixture import"

    def handle(self, *args, **options):
        user = get_user_model().objects.filter(is_superuser=True).first()
        adapter = SampleFixtureAdapter("fixtures/legacy_sample/sample_records.json")
        job = run_import(adapter, user)
        self.stdout.write(self.style.SUCCESS(f"Import completed: {job.summary}"))
