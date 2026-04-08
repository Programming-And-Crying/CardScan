import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_login_required_redirects(client):
    response = client.get(reverse("dashboard"))
    assert response.status_code == 302
    assert "/login/" in response.url


@pytest.mark.django_db
def test_readonly_cannot_create_contact(client, readonly_user):
    client.force_login(readonly_user)
    response = client.post(reverse("contacts:create"), {"full_name": "X"})
    assert response.status_code == 403
