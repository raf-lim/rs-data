from updaters.us.interfaces import UsMetric, Frequency, DataType, StatsType


class Metric(UsMetric):
    code: str = 'housing'
    name: str = 'Housing'
    constituents: dict[str, str] = {
        'PERMIT': 'Permits',
        'HOUST': 'Started',
        'COMPUTSA': 'Completed',
        }
    frequency: Frequency = Frequency.MONTHLY
    data: DataType = DataType.INDEX
    stats: StatsType = StatsType.CHANGE
    