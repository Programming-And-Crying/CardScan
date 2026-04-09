from __future__ import annotations

from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector, TrigramSimilarity
from django.db.models import Case, FloatField, Q, Value, When
from django.db.models.functions import Coalesce

from contacts.selectors import visible_contacts


def search_contacts_for_user(*, user, query: str):
    base = visible_contacts(user)
    q = (query or "").strip()
    if not q:
        return base.order_by("full_name")

    search_vector = (
        SearchVector("full_name", weight="A")
        + SearchVector("company", weight="A")
        + SearchVector("position", weight="B")
        + SearchVector("search_document", weight="C")
        + SearchVector("transliterated_text", weight="C")
    )
    search_query = SearchQuery(q)

    qs = (
        base.annotate(
            trigram_name=TrigramSimilarity("full_name", q),
            trigram_company=TrigramSimilarity("company", q),
            trigram_position=TrigramSimilarity("position", q),
            fts_rank=SearchRank(search_vector, search_query),
            exact_rank=Case(
                When(
                    Q(full_name__iexact=q)
                    | Q(company__iexact=q)
                    | Q(position__iexact=q)
                    | Q(contactemail__value__iexact=q)
                    | Q(contactphone__value__iexact=q),
                    then=Value(3.0),
                ),
                default=Value(0.0),
                output_field=FloatField(),
            ),
        )
        .annotate(
            combined_rank=Coalesce("exact_rank", Value(0.0))
            + Coalesce("trigram_name", Value(0.0))
            + Coalesce("trigram_company", Value(0.0))
            + Coalesce("trigram_position", Value(0.0))
            + Coalesce("fts_rank", Value(0.0))
        )
        .filter(
            Q(full_name__icontains=q)
            | Q(company__icontains=q)
            | Q(position__icontains=q)
            | Q(notes__icontains=q)
            | Q(transliterated_text__icontains=q)
            | Q(contactemail__value__icontains=q)
            | Q(contactphone__value__icontains=q)
            | Q(cards__ocr_raw__icontains=q)
            | Q(cards__xml_raw__icontains=q)
            | Q(combined_rank__gt=0.08)
        )
        .distinct()
        .order_by("-combined_rank", "full_name")
    )
    return qs
