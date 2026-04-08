import json
from pathlib import Path

from .base import LegacyRecord


class FixtureSampleAdapter:
    def __init__(self, fixture_path: Path):
        self.fixture_path = fixture_path

    def iter_records(self):
        rows = json.loads(self.fixture_path.read_text())
        for row in rows:
            yield LegacyRecord(**row)
