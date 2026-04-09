from uuid import UUID

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from accounts.permissions import can_mutate
from comments.forms import CommentForm
from comments.models import Comment
from history.models import ChangeHistory


@login_required
def add_comment(request, target_type: str, target_id: UUID):
    if not can_mutate(request.user):
        return HttpResponseForbidden()
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.target_type = target_type
        comment.target_id = target_id
        comment.created_by = request.user
        comment.save()
        ChangeHistory.objects.create(
            target_type=target_type,
            target_id=target_id,
            action_type="comment_created",
            actor=request.user,
            new_value_json={"comment_id": str(comment.id), "comment": comment.text},
        )
    return redirect(request.META.get("HTTP_REFERER", "/"))


@login_required
def edit_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk, is_deleted_soft=False)
    if not can_mutate(request.user):
        return HttpResponseForbidden()
    form = CommentForm(request.POST or None, instance=comment)
    if request.method == "POST" and form.is_valid():
        old = comment.text
        updated = form.save()
        ChangeHistory.objects.create(
            target_type=updated.target_type,
            target_id=updated.target_id,
            action_type="comment_updated",
            actor=request.user,
            old_value_json={"comment": old},
            new_value_json={"comment": updated.text},
        )
        return redirect(request.GET.get("next") or request.META.get("HTTP_REFERER", "/"))
    return render(request, "comments/form.html", {"form": form, "comment": comment})
