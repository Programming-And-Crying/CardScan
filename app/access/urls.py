from django.urls import path
from access.views import group_edit, groups_list

urlpatterns = [
    path("admin-ui/groups/", groups_list, name="groups_list"),
    path("admin-ui/groups/new/", group_edit, name="group_create"),
    path("admin-ui/groups/<uuid:pk>/", group_edit, name="group_edit"),
]
