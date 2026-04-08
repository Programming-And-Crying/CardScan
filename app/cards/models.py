import uuid
from django.conf import settings
from django.db import models


class ProcessingStatus(models.TextChoices):
    UPLOADED = "uploaded", "Uploaded"
    QUEUED = "queued", "Queued"
    PROCESSING = "processing", "Processing"
    PROCESSED = "processed", "Processed"
    NEEDS_REVIEW = "needs_review", "Needs Review"
    FAILED = "failed", "Failed"


class BusinessCard(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    contact = models.ForeignKey("contacts.Contact", null=True, blank=True, on_delete=models.SET_NULL, related_name="business_cards")
    original_file = models.FileField(upload_to="originals/%Y/%m/%d/")
    thumbnail_file = models.ImageField(upload_to="thumbnails/%Y/%m/%d/", blank=True)
    source_type = models.CharField(max_length=20, default="upload")
    legacy_external_id = models.CharField(max_length=255, blank=True)
    language_code = models.CharField(max_length=16, blank=True)
    language_confidence = models.FloatField(null=True, blank=True)
    xml_raw = models.TextField(blank=True)
    ocr_raw = models.TextField(blank=True)
    ocr_confidence = models.FloatField(null=True, blank=True)
    parsed_text = models.TextField(blank=True)
    normalized_text = models.TextField(blank=True)
    transliterated_text = models.TextField(blank=True)
    processing_status = models.CharField(max_length=32, choices=ProcessingStatus.choices, default=ProcessingStatus.UPLOADED)
    needs_manual_review = models.BooleanField(default=False)
    human_verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="cards_verified")
    verified_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="cards_created")
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="cards_updated")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ParsedField(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    target_type = models.CharField(max_length=40)
    target_id = models.UUIDField()
    field_name = models.CharField(max_length=80)
    field_value = models.TextField()
    field_source = models.CharField(max_length=20)
    confidence = models.FloatField(null=True, blank=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    target_type = models.CharField(max_length=40)
    target_id = models.UUIDField()
    text = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    is_deleted_soft = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ChangeHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    target_type = models.CharField(max_length=40)
    target_id = models.UUIDField()
    action_type = models.CharField(max_length=60)
    field_name = models.CharField(max_length=120, blank=True)
    old_value_json = models.JSONField(default=dict, blank=True)
    new_value_json = models.JSONField(default=dict, blank=True)
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)


class ProcessingTask(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    task_type = models.CharField(max_length=80)
    target_type = models.CharField(max_length=40)
    target_id = models.UUIDField()
    status = models.CharField(max_length=20, default="queued")
    attempts = models.PositiveIntegerField(default=0)
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True)
    metadata_json = models.JSONField(default=dict, blank=True)


class ImportJob(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    adapter_name = models.CharField(max_length=255)
    status = models.CharField(max_length=30, default="queued")
    started_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    metadata_json = models.JSONField(default=dict, blank=True)


class ImportJobRow(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job = models.ForeignKey(ImportJob, on_delete=models.CASCADE, related_name="rows")
    external_id = models.CharField(max_length=255)
    status = models.CharField(max_length=30)
    message = models.TextField(blank=True)
    contact = models.ForeignKey("contacts.Contact", null=True, blank=True, on_delete=models.SET_NULL)
    card = models.ForeignKey(BusinessCard, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
