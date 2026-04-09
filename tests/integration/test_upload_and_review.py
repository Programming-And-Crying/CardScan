import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from cards.models import BusinessCard


@pytest.mark.django_db
def test_upload_page_for_manager(client, manager_user):
    client.force_login(manager_user)
    response = client.get(reverse("upload_card"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_upload_card_creates_record(client, manager_user):
    client.force_login(manager_user)
    content = (
        b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
        b"\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDAT\x08\xd7c\xf8\xff\xff?\x00\x05\xfe\x02\xfeA\xe2(\x9d\x00\x00\x00\x00IEND\xaeB`\x82"
    )
    up = SimpleUploadedFile("card.png", content, content_type="image/png")
    response = client.post(reverse("upload_card"), {"original_file": up})
    assert response.status_code == 302
    card = BusinessCard.objects.latest("created_at")
    assert card.processing_status == BusinessCard.ProcessingStatus.QUEUED


@pytest.mark.django_db
def test_readonly_cannot_upload(client, readonly_user):
    client.force_login(readonly_user)
    response = client.get(reverse("upload_card"))
    assert response.status_code == 403
