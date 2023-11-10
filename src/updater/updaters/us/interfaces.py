from typing import Protocol, Optional
from enum import StrEnum, auto


class Frequency(StrEnum):
    DAILY = auto()
    WEEKLY = auto()
    MONTHLY = auto()
    QUARTERLY = auto()


class DataType(StrEnum):
    INDEX = auto()
    CHANGE = auto()


class StatsType(StrEnum):
    DIFFERENCE = auto()
    CHANGE = auto()


class Metric(Protocol):
    """Represents interface of US metric."""
    code: str
    name: str
    constituents: Optional[dict[str, str]]
    frequency: str
    data: Optional[DataType]
    stats: Optional[StatsType]