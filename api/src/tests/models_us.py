from sqlalchemy.orm import Mapped, mapped_column
from db.base_class import Base


class HousingData(Base):
    __tablename__ = "us_housing_data"
    date: Mapped[str] = mapped_column(primary_key=True)
    permits: Mapped[float] = mapped_column(nullable=True)
    started: Mapped[float] = mapped_column(nullable=True)
    completed: Mapped[float] = mapped_column(nullable=True)


class HousingStats(Base):
    __tablename__ = "us_housing_stats"
    index: Mapped[str] = mapped_column(primary_key=True)
    permits: Mapped[float] = mapped_column(nullable=True)
    started: Mapped[float] = mapped_column(nullable=True)
    completed: Mapped[float] = mapped_column(nullable=True)


class UsMetricsMetadata(Base):
    __tablename__ = "us_metrics_metadata"
    code: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]
    frequency: Mapped[str]
    data: Mapped[str]
    stats: Mapped[str]