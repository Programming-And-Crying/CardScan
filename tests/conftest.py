import pytest
from django.contrib.auth import get_user_model

from access.models import AccessGroup
from contacts.models import Contact


@pytest.fixture
def admin_user(db):
    return get_user_model().objects.create_user(username="admin", password="pass", role="admin")


@pytest.fixture
def office_user(db):
    return get_user_model().objects.create_user(username="office", password="pass", role="office_manager")


@pytest.fixture
def readonly_user(db):
    return get_user_model().objects.create_user(username="viewer", password="pass", role="readonly")


@pytest.fixture
def sales_group(db):
    return AccessGroup.objects.create(name="Sales", slug="sales")


@pytest.fixture
def visible_contact(db, admin_user, sales_group):
    contact = Contact.objects.create(full_name="Visible Contact", created_by=admin_user, updated_by=admin_user)
    contact.access_groups.add(sales_group)
    return contact
