from updaters.us.interfaces import UsMetric, Frequency, DataType, StatsType


class Metric(UsMetric):
    code: str = 'debt_gdp'
    name: str = 'Debt to GDP'
    constituents: dict[str, str] = {'GFDEGDQ188S': 'Debt to GDP',}
    frequency: Frequency = Frequency.QUARTERLY
    data: DataType = DataType.CHANGE
    stats: StatsType = StatsType.DIFFERENCE
