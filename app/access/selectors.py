from django.db.models import QuerySet

from accounts.models import Role, User
from contacts.models import Contact


def visible_contacts_for_user(user: User) -> QuerySet[Contact]:
    if user.role == Role.ADMIN:
        return Contact.objects.all().distinct()
    return Contact.objects.filter(access_groups__in=user.access_groups.filter(is_active=True)).distinct()
