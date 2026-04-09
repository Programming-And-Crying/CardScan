from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from accounts.permissions import can_mutate, is_admin
from comments.forms import CommentForm
from comments.models import Comment
from contacts.forms import ContactForm
from contacts.models import Contact
from contacts.search import search_contacts_for_user
from contacts.selectors import visible_contacts
from history.models import ChangeHistory


@login_required
def contacts_list(request):
    q = request.GET.get("q", "")
    queryset = search_contacts_for_user(user=request.user, query=q)
    return render(request, "contacts/list.html", {"contacts": queryset, "q": q})


@login_required
def contact_detail(request, pk):
    contact = get_object_or_404(visible_contacts(request.user), pk=pk)
    comments = Comment.objects.filter(target_type="contact", target_id=contact.id, is_deleted_soft=False)
    history = ChangeHistory.objects.filter(target_type="contact", target_id=contact.id).order_by("-created_at")[:30]
    return render(
        request,
        "contacts/detail.html",
        {"contact": contact, "comments": comments, "history": history, "form": CommentForm()},
    )


@login_required
def contact_create(request):
    if not can_mutate(request.user):
        return HttpResponseForbidden()
    form = ContactForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        contact = form.save(commit=False)
        contact.created_by = request.user
        contact.updated_by = request.user
        contact.save()
        form.save_m2m()
        ChangeHistory.objects.create(
            target_type="contact",
            target_id=contact.id,
            action_type="created",
            actor=request.user,
            new_value_json={"full_name": contact.full_name},
        )
        return redirect("contact_detail", pk=contact.pk)
    return render(request, "contacts/form.html", {"form": form})


@login_required
def contact_edit(request, pk):
    contact = get_object_or_404(visible_contacts(request.user), pk=pk)
    if not can_mutate(request.user):
        return HttpResponseForbidden()
    old = {
        "full_name": contact.full_name,
        "company": contact.company,
        "position": contact.position,
        "groups": list(contact.access_groups.values_list("slug", flat=True)),
    }
    form = ContactForm(request.POST or None, instance=contact)
    if request.method == "POST" and form.is_valid():
        updated = form.save(commit=False)
        updated.updated_by = request.user
        updated.save()
        form.save_m2m()
        ChangeHistory.objects.create(
            target_type="contact",
            target_id=contact.id,
            action_type="updated",
            actor=request.user,
            old_value_json=old,
            new_value_json={
                "full_name": updated.full_name,
                "company": updated.company,
                "position": updated.position,
                "groups": list(updated.access_groups.values_list("slug", flat=True)),
            },
        )
        return redirect("contact_detail", pk=contact.pk)
    return render(request, "contacts/form.html", {"form": form, "contact": contact})


@login_required
def contact_delete(request, pk):
    if not is_admin(request.user):
        return HttpResponseForbidden()
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == "POST":
        ChangeHistory.objects.create(
            target_type="contact",
            target_id=contact.id,
            action_type="deleted",
            actor=request.user,
            old_value_json={"full_name": contact.full_name},
        )
        contact.delete()
        return redirect("contacts_list")
    return render(request, "contacts/confirm_delete.html", {"contact": contact})
