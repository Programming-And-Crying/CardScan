import uuid
from django.db import models


class ProcessingTask(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    task_type = models.CharField(max_length=32)
    target_type = models.CharField(max_length=32)
    target_id = models.UUIDField()
    status = models.CharField(max_length=32, default="queued")
    attempts = models.PositiveIntegerField(default=0)
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True)
    metadata_json = models.JSONField(default=dict, blank=True)
