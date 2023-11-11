from updaters.us.interfaces import UsMetric, Frequency, DataType, StatsType


class Metric(UsMetric):
    code: str = 'jobs_nfp'
    name: str = 'Jobs NFP'
    constituents: dict[str, str] = {
        'PAYEMS': 'NFP',
        'CES0500000011': 'Weekly Earnings'
        }
    frequency: Frequency = Frequency.MONTHLY
    data: DataType = DataType.INDEX
    stats: StatsType = StatsType.DIFFERENCE
    