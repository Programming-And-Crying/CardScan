import uuid
from django.conf import settings
from django.db import models


class SourceType(models.TextChoices):
    MANUAL = "manual", "Manual"
    XML = "xml", "XML"
    OCR = "ocr", "OCR"
    GENERATED = "generated", "Generated"


class Contact(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=120, blank=True)
    last_name = models.CharField(max_length=120, blank=True)
    middle_name = models.CharField(max_length=120, blank=True)
    company = models.CharField(max_length=255, blank=True)
    position = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)
    normalized_text = models.TextField(blank=True)
    transliterated_text = models.TextField(blank=True)
    search_document = models.TextField(blank=True)
    access_groups = models.ManyToManyField("access.AccessGroup", related_name="contacts", blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="contacts_created")
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="contacts_updated")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["full_name"]

    def __str__(self) -> str:
        return self.full_name


class ContactAlias(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name="aliases")
    value = models.CharField(max_length=255)
    source = models.CharField(max_length=20, choices=SourceType.choices, default=SourceType.MANUAL)
    normalized_value = models.CharField(max_length=255, blank=True)
    transliterated_value = models.CharField(max_length=255, blank=True)


class ContactPhone(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name="phones")
    value = models.CharField(max_length=64)


class ContactEmail(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name="emails")
    value = models.EmailField()


class ContactWebsite(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name="websites")
    value = models.URLField()


class ContactAddress(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name="addresses")
    value = models.CharField(max_length=500)
