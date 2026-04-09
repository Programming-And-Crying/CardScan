from django.urls import path

from history.views import history_list

urlpatterns = [
    path("history/<str:entity>/<uuid:entity_id>/", history_list, name="history_list"),
]
