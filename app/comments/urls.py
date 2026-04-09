from django.urls import path

from comments.views import add_comment, edit_comment

urlpatterns = [
    path("comments/<str:target_type>/<uuid:target_id>/add/", add_comment, name="add_comment"),
    path("comments/<uuid:pk>/edit/", edit_comment, name="edit_comment"),
]
