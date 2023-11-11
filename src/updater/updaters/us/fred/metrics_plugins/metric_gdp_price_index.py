from updaters.us.interfaces import UsMetric, Frequency, DataType, StatsType


class Metric(UsMetric):
    code: str = 'gdp_price_index'
    name: str = 'GDP Price Index'
    constituents: dict[str, str] = {
        'GDPCTPI': 'GDP Price Index',
        'JCXFE': 'PCE Core Price Index',
    }
    frequency: Frequency = Frequency.QUARTERLY
    data: DataType = DataType.CHANGE
    stats: StatsType = StatsType.DIFFERENCE
