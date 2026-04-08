from django.urls import path

from .views import contact_create_view, contact_detail_view, contact_list_view

app_name = "contacts"

urlpatterns = [
    path("", contact_list_view, name="list"),
    path("create/", contact_create_view, name="create"),
    path("<uuid:pk>/", contact_detail_view, name="detail"),
]
