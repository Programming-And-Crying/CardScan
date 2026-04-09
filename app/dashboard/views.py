from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from cards.models import BusinessCard
from contacts.models import Contact


@login_required
def dashboard(request):
    context = {
        "contact_count": Contact.objects.count(),
        "card_count": BusinessCard.objects.count(),
        "needs_review_count": BusinessCard.objects.filter(needs_manual_review=True).count(),
    }
    return render(request, "dashboard/index.html", context)


def health_live(request):
    return HttpResponse("ok")


def health_ready(request):
    db_ok = True
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
    except Exception:
        db_ok = False
    status = 200 if db_ok else 503
    return JsonResponse({"status": "ready" if db_ok else "not_ready", "db": db_ok}, status=status)
