import base64
import json
from pathlib import Path

from imports.services import ImportRecord


class SampleFixtureAdapter:
    name = "sample_fixture"

    def __init__(self, fixture_file: str):
        self.fixture_file = Path(fixture_file)

    def iter_records(self):
        data = json.loads(self.fixture_file.read_text())
        for row in data:
            image_payload = row.get("image_base64", "")
            if not image_payload:
                raise ValueError("Fixture row missing image_base64")
            yield ImportRecord(
                external_id=row["external_id"],
                full_name=row["full_name"],
                company=row.get("company", ""),
                position=row.get("position", ""),
                xml_raw=row.get("xml_raw", ""),
                image_bytes=base64.b64decode(image_payload),
                image_name=row.get("image_name", "card.jpg"),
            )


class LegacyDbAdapter:
    """Placeholder for real legacy adapter. Requires schema and fixtures not yet available."""

    name = "legacy_db"

    def iter_records(self):
        raise NotImplementedError("Blocked until real legacy schema and sample DB dump are provided.")
