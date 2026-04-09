import pytest
from django.urls import reverse

from access.models import AccessGroup
from contacts.models import Contact
from contacts.search import search_contacts_for_user
from contacts.selectors import visible_contacts


@pytest.mark.django_db
def test_group_visibility(manager_user, admin_user, contact_visible):
    assert contact_visible in visible_contacts(manager_user)
    assert contact_visible in visible_contacts(admin_user)


@pytest.mark.django_db
def test_search_respects_group_visibility(manager_user):
    hidden_group = AccessGroup.objects.create(name="Hidden", slug="hidden")
    hidden = Contact.objects.create(full_name="Hidden Person", company="Nope")
    hidden.access_groups.add(hidden_group)
    visible = Contact.objects.create(full_name="Visible Person", company="Yep")
    visible.access_groups.add(*manager_user.access_groups.all())

    results = list(search_contacts_for_user(user=manager_user, query="Person"))
    assert visible in results
    assert hidden not in results


@pytest.mark.django_db
def test_contact_detail_forbidden_outside_group(client, manager_user):
    other_group = AccessGroup.objects.create(name="Other", slug="other")
    hidden = Contact.objects.create(full_name="Secret")
    hidden.access_groups.add(other_group)

    client.force_login(manager_user)
    response = client.get(reverse("contact_detail", kwargs={"pk": hidden.id}))
    assert response.status_code == 404
