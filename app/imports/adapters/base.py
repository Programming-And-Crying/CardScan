from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Protocol


@dataclass
class LegacyRecord:
    external_id: str
    full_name: str
    company: str
    position: str
    image_path: str
    xml_raw: str
    email: str = ""
    phone: str = ""


class LegacyAdapter(Protocol):
    def iter_records(self) -> Iterable[LegacyRecord]: ...


class RealLegacyAdapterPlaceholder:
    """Placeholder for the real historical DB adapter.

    Blocked by missing source schema and production-like fixtures.
    """

    def iter_records(self) -> Iterable[LegacyRecord]:
        raise NotImplementedError("Real legacy adapter requires schema + sample dataset")
