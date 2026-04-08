from django.urls import path

from .views import group_create_view, groups_list_view

app_name = "access"

urlpatterns = [
    path("", groups_list_view, name="group-list"),
    path("create/", group_create_view, name="group-create"),
]
