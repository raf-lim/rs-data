from typing import Protocol, Optional
from enum import Enum, auto


class Frequency(Enum):
    DAILY = 'd'
    WEEKLY = 'w'
    MONTHLY = 'm'
    QUARTERLY = 'q'


class TableType(Enum):
    INDEX = auto()
    CHANGE = auto()


class StatsType(Enum):
    DIFFERENCE = auto()
    CHANGE = auto()


class Metric(Protocol):
    """Represents interface of US metric."""
    code: str
    name: str
    constituents: Optional[dict[str, str]]
    frequency: str
    table: Optional[tuple[TableType, StatsType]]