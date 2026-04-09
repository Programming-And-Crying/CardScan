from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render

from accounts.permissions import is_admin
from imports.adapters import SampleFixtureAdapter
from imports.models import ImportJob
from imports.services import run_import


@login_required
def imports_list(request):
    if not is_admin(request.user):
        return HttpResponseForbidden()
    return render(request, "admin_ui/imports.html", {"jobs": ImportJob.objects.order_by("-created_at")[:100]})


@login_required
def imports_run_sample(request):
    if not is_admin(request.user):
        return HttpResponseForbidden()
    if request.method == "POST":
        adapter = SampleFixtureAdapter("fixtures/legacy_sample/sample_records.json")
        run_import(adapter, request.user)
    return redirect("imports_list")
