from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, render

from access.selectors import visible_contacts_for_user

from .models import BusinessCard


@login_required
def card_detail_view(request, pk):
    card = get_object_or_404(BusinessCard, pk=pk)
    if card.contact and not visible_contacts_for_user(request.user).filter(pk=card.contact_id).exists():
        raise Http404("Card not found")
    return render(request, "cards/detail.html", {"card": card})
