from django.urls import path

from .views import card_detail_view

app_name = "cards"

urlpatterns = [
    path("<uuid:pk>/", card_detail_view, name="detail"),
]
