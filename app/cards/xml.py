from __future__ import annotations

from dataclasses import dataclass
import xml.etree.ElementTree as ET


@dataclass
class XmlParsedData:
    name: str = ""
    company: str = ""
    position: str = ""
    email: str = ""
    phone: str = ""


def parse_card_xml(xml_raw: str) -> XmlParsedData:
    if not xml_raw.strip():
        return XmlParsedData()
    try:
        root = ET.fromstring(xml_raw)
    except ET.ParseError:
        return XmlParsedData()

    def _txt(tag: str) -> str:
        el = root.find(tag)
        return (el.text or "").strip() if el is not None else ""

    return XmlParsedData(
        name=_txt("name"),
        company=_txt("company"),
        position=_txt("position"),
        email=_txt("email"),
        phone=_txt("phone"),
    )
