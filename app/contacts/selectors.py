from django.contrib.auth import get_user_model

from contacts.models import Contact


User = get_user_model()


def visible_contacts(user: User):
    if not user.is_authenticated:
        return Contact.objects.none()
    if user.role == "admin":
        return Contact.objects.all().prefetch_related("access_groups")
    return Contact.objects.filter(access_groups__in=user.access_groups.all()).distinct().prefetch_related("access_groups")
