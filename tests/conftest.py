import pytest
from django.contrib.auth import get_user_model

from access.models import AccessGroup
from contacts.models import Contact


@pytest.fixture
def group_a(db):
    return AccessGroup.objects.create(name="A", slug="a")


@pytest.fixture
def admin_user(db):
    User = get_user_model()
    user = User.objects.create_user(username="admin", password="pass", role="admin")
    return user


@pytest.fixture
def manager_user(db, group_a):
    User = get_user_model()
    user = User.objects.create_user(username="manager", password="pass", role="office_manager")
    user.access_groups.add(group_a)
    return user


@pytest.fixture
def readonly_user(db, group_a):
    User = get_user_model()
    user = User.objects.create_user(username="reader", password="pass", role="readonly")
    user.access_groups.add(group_a)
    return user


@pytest.fixture
def contact_visible(db, manager_user, group_a):
    c = Contact.objects.create(full_name="Visible Contact", company="ACME", created_by=manager_user)
    c.access_groups.add(group_a)
    return c
