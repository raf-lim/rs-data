from updaters.us.interfaces import UsMetric, Frequency, DataType, StatsType


class Metric(UsMetric):
    code: str = 'fed'
    name: str = 'FED Funds Rate'
    constituents: dict[str, str] = {'FEDFUNDS': 'FED Funds'}
    frequency: Frequency = Frequency.MONTHLY
    data: DataType = DataType.INDEX
    stats: StatsType = StatsType.DIFFERENCE
