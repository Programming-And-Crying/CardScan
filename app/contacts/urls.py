from django.urls import path

from contacts.views import contact_create, contact_delete, contact_detail, contact_edit, contacts_list

urlpatterns = [
    path("contacts/", contacts_list, name="contacts_list"),
    path("contacts/new/", contact_create, name="contact_create"),
    path("contacts/<uuid:pk>/", contact_detail, name="contact_detail"),
    path("contacts/<uuid:pk>/edit/", contact_edit, name="contact_edit"),
    path("contacts/<uuid:pk>/delete/", contact_delete, name="contact_delete"),
]
