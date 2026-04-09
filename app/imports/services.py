from dataclasses import dataclass
from typing import Protocol

from django.core.files.base import ContentFile

from cards.models import BusinessCard
from contacts.models import Contact
from imports.models import ImportJob, ImportJobRow


@dataclass
class ImportRecord:
    external_id: str
    full_name: str
    company: str
    position: str
    xml_raw: str
    image_bytes: bytes
    image_name: str = "card.jpg"


class ImportAdapter(Protocol):
    name: str

    def iter_records(self): ...


def run_import(adapter: ImportAdapter, user=None) -> ImportJob:
    job = ImportJob.objects.create(adapter_name=adapter.name, created_by=user)
    ok = 0
    failed = 0
    for record in adapter.iter_records():
        try:
            contact, _ = Contact.objects.get_or_create(
                full_name=record.full_name,
                defaults={
                    "company": record.company,
                    "position": record.position,
                    "created_by": user,
                    "updated_by": user,
                },
            )
            card = BusinessCard(
                contact=contact,
                source_type="legacy_import",
                xml_raw=record.xml_raw,
                legacy_external_id=record.external_id,
                created_by=user,
                updated_by=user,
            )
            card.original_file.save(
                f"import-{record.external_id}-{record.image_name}",
                ContentFile(record.image_bytes),
                save=True,
            )
            ImportJobRow.objects.create(job=job, external_id=record.external_id, status="success")
            ok += 1
        except Exception as exc:
            ImportJobRow.objects.create(
                job=job, external_id=record.external_id, status="failed", message=str(exc)
            )
            failed += 1
    job.status = "completed"
    job.summary = {"success": ok, "failed": failed}
    job.save(update_fields=["status", "summary"])
    return job
