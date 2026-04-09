import uuid
from django.conf import settings
from django.db import models

from contacts.models import Contact


class BusinessCard(models.Model):
    class ProcessingStatus(models.TextChoices):
        UPLOADED = "uploaded", "Uploaded"
        QUEUED = "queued", "Queued"
        PROCESSING = "processing", "Processing"
        PROCESSED = "processed", "Processed"
        NEEDS_REVIEW = "needs_review", "Needs review"
        FAILED = "failed", "Failed"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    contact = models.ForeignKey(Contact, null=True, blank=True, on_delete=models.SET_NULL, related_name="cards")
    original_file = models.ImageField(upload_to="originals/%Y/%m/%d/")
    thumbnail_file = models.ImageField(upload_to="thumbnails/%Y/%m/%d/", blank=True)
    source_type = models.CharField(max_length=32, default="upload")
    legacy_external_id = models.CharField(max_length=255, blank=True)
    language_code = models.CharField(max_length=32, blank=True)
    language_confidence = models.FloatField(null=True, blank=True)
    xml_raw = models.TextField(blank=True)
    ocr_raw = models.TextField(blank=True)
    ocr_confidence = models.FloatField(null=True, blank=True)
    parsed_text = models.TextField(blank=True)
    normalized_text = models.TextField(blank=True)
    transliterated_text = models.TextField(blank=True)
    processing_status = models.CharField(max_length=32, choices=ProcessingStatus.choices, default=ProcessingStatus.UPLOADED)
    needs_manual_review = models.BooleanField(default=True)
    human_verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="verified_cards")
    verified_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="created_cards")
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="updated_cards")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ParsedField(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    target_type = models.CharField(max_length=32)
    target_id = models.UUIDField()
    field_name = models.CharField(max_length=100)
    field_value = models.TextField()
    field_source = models.CharField(max_length=32)
    confidence = models.FloatField(null=True, blank=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
