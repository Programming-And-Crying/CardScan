from pathlib import Path
from shutil import copy2

from cards.models import BusinessCard, ImportJob, ImportJobRow
from contacts.models import Contact, ContactEmail, ContactPhone


def run_import(adapter, started_by=None) -> ImportJob:
    job = ImportJob.objects.create(adapter_name=adapter.__class__.__name__, started_by=started_by, status="running")
    for record in adapter.iter_records():
        try:
            contact, _ = Contact.objects.get_or_create(
                full_name=record.full_name,
                defaults={"company": record.company, "position": record.position, "created_by": started_by, "updated_by": started_by},
            )
            if record.email:
                ContactEmail.objects.get_or_create(contact=contact, value=record.email)
            if record.phone:
                ContactPhone.objects.get_or_create(contact=contact, value=record.phone)

            img = Path(record.image_path)
            card = BusinessCard.objects.create(
                contact=contact,
                source_type="legacy_import",
                legacy_external_id=record.external_id,
                xml_raw=record.xml_raw,
                processing_status="queued",
            )
            with img.open("rb") as fh:
                card.original_file.save(img.name, fh, save=True)

            ImportJobRow.objects.create(job=job, external_id=record.external_id, status="success", contact=contact, card=card)
        except Exception as exc:
            ImportJobRow.objects.create(job=job, external_id=record.external_id, status="failed", message=str(exc))
    job.status = "finished"
    job.save(update_fields=["status"])
    return job
