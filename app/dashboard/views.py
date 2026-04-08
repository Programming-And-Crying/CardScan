from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render


@login_required
def dashboard_view(request):
    return render(request, "dashboard/index.html")


def live_health_view(request):
    return JsonResponse({"status": "ok"})


def ready_health_view(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
    except Exception:
        return JsonResponse({"status": "not_ready"}, status=503)
    return JsonResponse({"status": "ready"})
