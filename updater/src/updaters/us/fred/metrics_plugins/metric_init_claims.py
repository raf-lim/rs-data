from updaters.us.interfaces import UsMetric, Frequency, DataType, StatsType


class Metric(UsMetric):
    code: str = 'init_claims'
    name: str = 'Initial Claims'
    constituents: dict[str, str] = {'ICSA': 'Initial Claims'}
    frequency: Frequency = Frequency.WEEKLY
    data: DataType = DataType.INDEX
    stats: StatsType = StatsType.DIFFERENCE
