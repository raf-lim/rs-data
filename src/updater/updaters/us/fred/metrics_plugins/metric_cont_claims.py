from updaters.us.interfaces import UsMetric, Frequency, DataType, StatsType


class Metric(UsMetric):
    code: str = 'cont_claims'
    name: str = 'Continued Claims'
    constituents: dict[str, str] = {'CCSA': 'Continued Claims'}
    frequency: Frequency = Frequency.WEEKLY
    data: DataType = DataType.INDEX
    stats: StatsType = StatsType.DIFFERENCE
