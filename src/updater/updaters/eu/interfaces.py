from typing import Protocol


class EsiMetric(Protocol):
    code: str
    name: str