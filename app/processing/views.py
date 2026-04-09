from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render

from accounts.permissions import is_admin
from processing.models import ProcessingTask


@login_required
def tasks_list(request):
    if not is_admin(request.user):
        return HttpResponseForbidden()
    return render(request, "admin_ui/tasks.html", {"tasks": ProcessingTask.objects.order_by("-id")[:200]})


@login_required
def system_status(request):
    if not is_admin(request.user):
        return HttpResponseForbidden()
    return render(request, "admin_ui/system.html")
