from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from access.selectors import visible_contacts_for_user
from accounts.permissions import require_editor

from .forms import ContactForm
from .models import Contact


@login_required
def contact_list_view(request):
    contacts = visible_contacts_for_user(request.user)
    return render(request, "contacts/list.html", {"contacts": contacts})


@login_required
def contact_detail_view(request, pk):
    contact = get_object_or_404(visible_contacts_for_user(request.user), pk=pk)
    return render(request, "contacts/detail.html", {"contact": contact})


@login_required
def contact_create_view(request):
    require_editor(request.user)
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.created_by = request.user
            contact.updated_by = request.user
            contact.save()
            form.save_m2m()
            return redirect("contacts:detail", pk=contact.pk)
    else:
        form = ContactForm()
    return render(request, "contacts/form.html", {"form": form, "mode": "create"})
