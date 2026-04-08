from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from accounts.permissions import require_admin

from .forms import AccessGroupForm
from .models import AccessGroup


@login_required
def groups_list_view(request):
    require_admin(request.user)
    return render(request, "access/groups_list.html", {"groups": AccessGroup.objects.all()})


@login_required
def group_create_view(request):
    require_admin(request.user)
    if request.method == "POST":
        form = AccessGroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("access:group-list")
    else:
        form = AccessGroupForm()
    return render(request, "access/group_form.html", {"form": form})
