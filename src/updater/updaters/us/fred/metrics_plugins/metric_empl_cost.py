from updaters.us.interfaces import UsMetric, Frequency, DataType, StatsType


class Metric(UsMetric):
    code: str = 'empl_cost'
    name: str = 'Employment Cost Index'
    constituents: dict[str, str] = {'ECIALLCIV': 'Employment Cost Index'}
    frequency: Frequency = Frequency.QUARTERLY
    data: DataType = DataType.CHANGE
    stats: StatsType = StatsType.DIFFERENCE