from celery import shared_task
from PIL import Image
import pytesseract

from cards.models import BusinessCard
from cards.services import detect_language, extract_candidate_fields, normalize_and_transliterate
from cards.xml import parse_card_xml
from processing.models import ProcessingTask


@shared_task
def process_card(card_id: str) -> None:
    card = BusinessCard.objects.get(pk=card_id)
    task = ProcessingTask.objects.create(
        task_type="ocr",
        target_type="card",
        target_id=card.id,
        status="processing",
    )
    try:
        card.processing_status = BusinessCard.ProcessingStatus.PROCESSING
        card.save(update_fields=["processing_status"])

        text = pytesseract.image_to_string(Image.open(card.original_file.path))
        card.ocr_raw = text

        lang, conf = detect_language(text)
        card.language_code = lang
        card.language_confidence = conf
        card.normalized_text, card.transliterated_text = normalize_and_transliterate(text)

        ocr_fields = extract_candidate_fields(text)
        xml_fields = parse_card_xml(card.xml_raw)
        combined = {
            **{k: v for k, v in ocr_fields.items() if v},
            **{k: v for k, v in xml_fields.__dict__.items() if v},
        }

        manual_prefix = "MANUAL:"
        if not card.parsed_text.startswith(manual_prefix):
            card.parsed_text = "\n".join(f"{k}: {v}" for k, v in combined.items() if v)

        has_key = bool(combined.get("email") or combined.get("phone"))
        card.needs_manual_review = not has_key
        card.processing_status = (
            BusinessCard.ProcessingStatus.NEEDS_REVIEW
            if card.needs_manual_review
            else BusinessCard.ProcessingStatus.PROCESSED
        )
        card.save()

        task.status = "done"
        task.metadata_json = combined
        task.save(update_fields=["status", "metadata_json"])
    except Exception as exc:
        card.processing_status = BusinessCard.ProcessingStatus.FAILED
        card.needs_manual_review = True
        card.save(update_fields=["processing_status", "needs_manual_review"])
        task.status = "failed"
        task.error_message = str(exc)
        task.save(update_fields=["status", "error_message"])
        raise
