from updaters.us.interfaces import UsMetric, Frequency, DataType, StatsType


class Metric(UsMetric):
    code: str = 'money'
    name: str = 'Money Stock'
    constituents: dict[str, str] = {
        'WM1NS': 'M1',
        'WM2NS': 'M2',
        }
    frequency: Frequency = Frequency.WEEKLY
    data: DataType = DataType.CHANGE
    stats: StatsType = StatsType.DIFFERENCE
