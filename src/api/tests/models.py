from sqlalchemy.orm import Mapped, mapped_column
from db.base_class import Base


class EsiData(Base):
    __tablename__ = "eu_metric_esi_data"
    date: Mapped[str] = mapped_column(primary_key=True)
    PL_ESI: Mapped[float] = mapped_column(nullable=True)
    FR_ESI: Mapped[float] = mapped_column(nullable=True)
    DK_ESI: Mapped[float] = mapped_column(nullable=True)


class InduData(Base):
    __tablename__ = "eu_metric_indu_data"
    date: Mapped[str] = mapped_column(primary_key=True)
    PL_INDU: Mapped[float] = mapped_column(nullable=True)
    FR_INDU: Mapped[float] = mapped_column(nullable=True)
    DK_INDU: Mapped[float] = mapped_column(nullable=True)


class ServData(Base):
    __tablename__ = "eu_metric_serv_data"
    date: Mapped[str] = mapped_column(primary_key=True)
    PL_SERV: Mapped[float] = mapped_column(nullable=True)
    FR_SERV: Mapped[float] = mapped_column(nullable=True)
    DK_SERV: Mapped[float] = mapped_column(nullable=True) 


class EsiStats(Base):
    __tablename__ = "eu_metric_esi_stats"
    stat: Mapped[str] = mapped_column(primary_key=True)
    PL_ESI: Mapped[float] = mapped_column(nullable=True)
    FR_ESI: Mapped[float] = mapped_column(nullable=True)
    DK_ESI: Mapped[float] = mapped_column(nullable=True)


class InduStats(Base):
    __tablename__ = "eu_metric_indu_stats"
    stat: Mapped[str] = mapped_column(primary_key=True)
    PL_INDU: Mapped[float] = mapped_column(nullable=True)
    FR_INDU: Mapped[float] = mapped_column(nullable=True)
    DK_INDU: Mapped[float] = mapped_column(nullable=True)


class PlData(Base):
    __tablename__ = "eu_country_pl_data"
    date: Mapped[str] = mapped_column(primary_key=True)
    PL_ESI: Mapped[float] = mapped_column(nullable=True)
    PL_INDU: Mapped[float] = mapped_column(nullable=True)


class FrData(Base):
    __tablename__ = "eu_country_fr_data"
    date: Mapped[str] = mapped_column(primary_key=True)
    FR_ESI: Mapped[float]
    FR_INDU: Mapped[float]


class DkData(Base):
    __tablename__ = "eu_country_dk_data"
    date: Mapped[str] = mapped_column(primary_key=True)
    DK_ESI: Mapped[float]
    DK_INDU: Mapped[float]