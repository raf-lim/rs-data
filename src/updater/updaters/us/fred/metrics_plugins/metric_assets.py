from updaters.us.interfaces import UsMetric, Frequency, DataType, StatsType


class Metric(UsMetric):
    code: str = 'assets'
    name: str = 'Total Assets'
    constituents: dict[str, str] = {'WALCL': 'Total Assets',}
    frequency: Frequency = Frequency.WEEKLY
    data: DataType = DataType.CHANGE
    stats: StatsType = StatsType.DIFFERENCE
