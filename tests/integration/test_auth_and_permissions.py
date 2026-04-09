import pytest
from django.urls import reverse

from contacts.models import Contact


@pytest.mark.django_db
def test_login_required_redirect(client):
    response = client.get(reverse("contacts_list"))
    assert response.status_code == 302
    assert "/login/" in response.url


@pytest.mark.django_db
def test_login_and_logout_flow(client, readonly_user):
    response = client.post(reverse("login"), {"username": readonly_user.username, "password": "pass"})
    assert response.status_code == 302
    response = client.post(reverse("logout"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_readonly_cannot_create_contact(client, readonly_user):
    client.force_login(readonly_user)
    response = client.post(reverse("contact_create"), {"full_name": "X"})
    assert response.status_code == 403


@pytest.mark.django_db
def test_admin_can_delete_contact(client, admin_user):
    contact = Contact.objects.create(full_name="Delete Me")
    client.force_login(admin_user)
    response = client.post(reverse("contact_delete", kwargs={"pk": contact.id}))
    assert response.status_code == 302
    assert not Contact.objects.filter(pk=contact.id).exists()
