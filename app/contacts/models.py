import uuid
from django.conf import settings
from django.db import models
from django.utils.text import slugify
from unidecode import unidecode

from access.models import AccessGroup


class Contact(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    middle_name = models.CharField(max_length=255, blank=True)
    company = models.CharField(max_length=255, blank=True)
    position = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)
    normalized_text = models.TextField(blank=True)
    transliterated_text = models.TextField(blank=True)
    search_document = models.TextField(blank=True)
    access_groups = models.ManyToManyField(AccessGroup, blank=True, related_name="contacts")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="created_contacts")
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="updated_contacts")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def refresh_search_fields(self) -> None:
        values = [self.full_name, self.company, self.position, self.notes]
        self.normalized_text = " ".join(slugify(v, allow_unicode=True) for v in values if v)
        self.transliterated_text = " ".join(unidecode(v) for v in values if v)
        self.search_document = " ".join(v for v in values if v)

    def save(self, *args, **kwargs):
        self.refresh_search_fields()
        return super().save(*args, **kwargs)


class ContactValueBase(models.Model):
    SOURCE_CHOICES = (("manual", "Manual"), ("xml", "XML"), ("ocr", "OCR"), ("generated", "Generated"))
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    value = models.CharField(max_length=255)
    source = models.CharField(max_length=16, choices=SOURCE_CHOICES, default="manual")
    normalized_value = models.CharField(max_length=255, blank=True)
    transliterated_value = models.CharField(max_length=255, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.normalized_value = slugify(self.value, allow_unicode=True)
        self.transliterated_value = unidecode(self.value)
        super().save(*args, **kwargs)


class ContactAlias(ContactValueBase):
    pass


class ContactPhone(ContactValueBase):
    pass


class ContactEmail(ContactValueBase):
    pass


class ContactWebsite(ContactValueBase):
    pass


class ContactAddress(ContactValueBase):
    pass
