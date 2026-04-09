from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from accounts.permissions import is_admin
from access.forms import AccessGroupForm
from access.models import AccessGroup


@login_required
def groups_list(request):
    if not is_admin(request.user):
        return HttpResponseForbidden()
    return render(request, "admin_ui/groups.html", {"groups": AccessGroup.objects.all()})


@login_required
def group_edit(request, pk=None):
    if not is_admin(request.user):
        return HttpResponseForbidden()
    instance = get_object_or_404(AccessGroup, pk=pk) if pk else None
    form = AccessGroupForm(request.POST or None, instance=instance)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("groups_list")
    return render(request, "admin_ui/group_form.html", {"form": form})
