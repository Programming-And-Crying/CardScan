from django.urls import path

from accounts.views import user_create, user_edit, users_list

urlpatterns = [
    path("admin-ui/users/", users_list, name="users_list"),
    path("admin-ui/users/new/", user_create, name="user_create"),
    path("admin-ui/users/<int:pk>/", user_edit, name="user_edit"),
]
