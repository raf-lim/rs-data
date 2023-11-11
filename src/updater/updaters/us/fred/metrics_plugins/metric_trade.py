from updaters.us.interfaces import UsMetric, Frequency, DataType, StatsType


class Metric(UsMetric):
    code: str = 'trade'
    name: str = 'Trade Balance'
    constituents: dict[str, str] = {'BOPGSTB': 'Trade Balance'}
    frequency: Frequency = Frequency.MONTHLY
    data: DataType = DataType.INDEX
    stats: StatsType = StatsType.CHANGE
