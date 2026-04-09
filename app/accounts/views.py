from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from accounts.forms import UserAdminForm
from accounts.models import User
from accounts.permissions import is_admin


@login_required
def users_list(request):
    if not is_admin(request.user):
        return HttpResponseForbidden()
    return render(request, "admin_ui/users.html", {"users": User.objects.all().order_by("username")})


@login_required
def user_create(request):
    if not is_admin(request.user):
        return HttpResponseForbidden()
    form = UserAdminForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save(commit=False)
        user.set_password("password123")
        user.save()
        form.save_m2m()
        return redirect("users_list")
    return render(request, "admin_ui/user_form.html", {"form": form, "target_user": None})


@login_required
def user_edit(request, pk):
    if not is_admin(request.user):
        return HttpResponseForbidden()
    user = get_object_or_404(User, pk=pk)
    form = UserAdminForm(request.POST or None, instance=user)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("users_list")
    return render(request, "admin_ui/user_form.html", {"form": form, "target_user": user})
