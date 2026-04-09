from uuid import UUID
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from history.models import ChangeHistory


@login_required
def history_list(request, entity: str, entity_id: UUID):
    items = ChangeHistory.objects.filter(target_type=entity, target_id=entity_id).order_by("-created_at")
    return render(request, "history/list.html", {"items": items, "entity": entity})
