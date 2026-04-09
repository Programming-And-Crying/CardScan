from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from accounts.permissions import can_mutate, is_admin
from cards.forms import CardReviewForm, CardUploadForm
from cards.models import BusinessCard
from cards.tasks import process_card
from comments.forms import CommentForm
from comments.models import Comment
from contacts.selectors import visible_contacts
from history.models import ChangeHistory


def _can_access_card(user, card: BusinessCard) -> bool:
    if user.role == "admin":
        return True
    if not card.contact_id:
        return user.role in {"admin", "office_manager"}
    return visible_contacts(user).filter(pk=card.contact_id).exists()


@login_required
def card_detail(request, pk):
    card = get_object_or_404(BusinessCard, pk=pk)
    if not _can_access_card(request.user, card):
        return HttpResponseForbidden()
    comments = Comment.objects.filter(target_type="card", target_id=card.id, is_deleted_soft=False)
    history = ChangeHistory.objects.filter(target_type="card", target_id=card.id).order_by("-created_at")[:30]
    return render(
        request,
        "cards/detail.html",
        {"card": card, "comments": comments, "history": history, "form": CommentForm()},
    )


@login_required
def upload_card(request):
    if not can_mutate(request.user):
        return HttpResponseForbidden()
    form = CardUploadForm(request.POST or None, request.FILES or None)
    form.fields["contact"].queryset = visible_contacts(request.user)
    if request.method == "POST" and form.is_valid():
        card = form.save(commit=False)
        card.created_by = request.user
        card.updated_by = request.user
        card.processing_status = BusinessCard.ProcessingStatus.QUEUED
        card.needs_manual_review = True
        card.save()
        process_card.delay(str(card.id))
        ChangeHistory.objects.create(
            target_type="card",
            target_id=card.id,
            action_type="uploaded",
            actor=request.user,
            new_value_json={"status": card.processing_status},
        )
        return redirect("card_detail", pk=card.pk)
    return render(request, "upload/form.html", {"form": form})


@login_required
def card_edit(request, pk):
    card = get_object_or_404(BusinessCard, pk=pk)
    if not can_mutate(request.user) or not _can_access_card(request.user, card):
        return HttpResponseForbidden()
    old = {
        "human_verified": card.human_verified,
        "needs_manual_review": card.needs_manual_review,
        "contact": str(card.contact_id) if card.contact_id else None,
    }
    form = CardReviewForm(request.POST or None, instance=card)
    form.fields["contact"].queryset = visible_contacts(request.user)
    if request.method == "POST" and form.is_valid():
        updated = form.save(commit=False)
        updated.updated_by = request.user
        if updated.parsed_text and not updated.parsed_text.startswith("MANUAL:"):
            updated.parsed_text = f"MANUAL:{updated.parsed_text}"
        if updated.human_verified and not updated.verified_at:
            updated.verified_at = timezone.now()
            updated.verified_by = request.user
        if not updated.human_verified:
            updated.verified_at = None
            updated.verified_by = None
        updated.save()
        ChangeHistory.objects.create(
            target_type="card",
            target_id=card.id,
            action_type="updated",
            actor=request.user,
            old_value_json=old,
            new_value_json={
                "human_verified": updated.human_verified,
                "needs_manual_review": updated.needs_manual_review,
                "contact": str(updated.contact_id) if updated.contact_id else None,
            },
        )
        return redirect("card_detail", pk=card.pk)
    return render(request, "cards/form.html", {"form": form, "card": card})


@login_required
def card_delete(request, pk):
    if not is_admin(request.user):
        return HttpResponseForbidden()
    card = get_object_or_404(BusinessCard, pk=pk)
    if request.method == "POST":
        ChangeHistory.objects.create(
            target_type="card",
            target_id=card.id,
            action_type="deleted",
            actor=request.user,
            old_value_json={"contact": str(card.contact_id) if card.contact_id else None},
        )
        card.delete()
        return redirect("contacts_list")
    return render(request, "cards/confirm_delete.html", {"card": card})


@login_required
def review_queue(request):
    cards = BusinessCard.objects.filter(needs_manual_review=True).order_by("-created_at")
    if request.user.role != "admin":
        cards = cards.filter(contact__in=visible_contacts(request.user)) | cards.filter(contact__isnull=True)
    hv = request.GET.get("human_verified")
    if hv in {"true", "false"}:
        cards = cards.filter(human_verified=(hv == "true"))
    failed = request.GET.get("failed")
    if failed == "1":
        cards = cards.filter(processing_status=BusinessCard.ProcessingStatus.FAILED)
    return render(request, "review/queue.html", {"cards": cards.distinct()[:200]})
