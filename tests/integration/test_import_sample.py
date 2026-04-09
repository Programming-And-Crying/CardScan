import pytest
from imports.adapters import SampleFixtureAdapter
from imports.services import run_import


@pytest.mark.django_db
def test_sample_import(admin_user):
    job = run_import(SampleFixtureAdapter("fixtures/legacy_sample/sample_records.json"), admin_user)
    assert job.summary["success"] >= 1
