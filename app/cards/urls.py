from django.urls import path

from cards.views import card_delete, card_detail, card_edit, review_queue, upload_card

urlpatterns = [
    path("cards/<uuid:pk>/", card_detail, name="card_detail"),
    path("cards/<uuid:pk>/edit/", card_edit, name="card_edit"),
    path("cards/<uuid:pk>/delete/", card_delete, name="card_delete"),
    path("upload/", upload_card, name="upload_card"),
    path("review-queue/", review_queue, name="review_queue"),
]
