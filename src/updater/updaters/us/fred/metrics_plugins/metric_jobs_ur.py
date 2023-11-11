from updaters.us.interfaces import UsMetric, Frequency, DataType, StatsType


class Metric(UsMetric):
    code: str = 'jobs_ur'
    name: str = 'Jobs UR'
    constituents: dict[str, str] = {
        'UNRATE': 'UR',
        'CIVPART': 'Participation Rate'
        }
    frequency: Frequency = Frequency.MONTHLY
    data: DataType = DataType.INDEX
    stats: StatsType = StatsType.DIFFERENCE
