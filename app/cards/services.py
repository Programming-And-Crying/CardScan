import re
from unidecode import unidecode
from langdetect import detect, DetectorFactory

DetectorFactory.seed = 0


def extract_candidate_fields(text: str) -> dict[str, str]:
    email = re.search(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", text)
    phone = re.search(r"\+?[0-9][0-9\- ()]{7,}", text)
    website = re.search(r"https?://\S+|www\.\S+", text)
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return {
        "email": email.group(0) if email else "",
        "phone": phone.group(0) if phone else "",
        "website": website.group(0) if website else "",
        "candidate_name": lines[0] if lines else "",
        "candidate_company": lines[1] if len(lines) > 1 else "",
    }


def detect_language(text: str) -> tuple[str, float]:
    if not text.strip():
        return "", 0.0
    try:
        return detect(text), 0.5
    except Exception:
        return "", 0.0


def normalize_and_transliterate(text: str) -> tuple[str, str]:
    return text.lower(), unidecode(text)
