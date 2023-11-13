from updaters.us.interfaces import UsMetric, Frequency, DataType, StatsType


class Metric(UsMetric):
    code: str = 'gdp'
    name: str = 'GDP'
    constituents: dict[str, str] = {
        'GDPC1': 'Real GDP',
        'PCECC96': 'Consumption',
        'GPDIC1': 'Investments',
        'GCEC1': 'Government',
        'IMPGSC1': 'Imports',
        'EXPGSC1': 'Exports',
    }
    frequency: Frequency = Frequency.QUARTERLY
    data: DataType = DataType.CHANGE
    stats: StatsType = StatsType.DIFFERENCE