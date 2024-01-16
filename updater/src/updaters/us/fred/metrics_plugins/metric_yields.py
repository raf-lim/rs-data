from updaters.us.interfaces import UsMetric, Frequency, DataType, StatsType


class Metric(UsMetric):
    code: str = 'yields'
    name: str = 'Bond Yields'
    constituents: dict[str, str] = {
        'T10Y2Y': '10Y_2Y',
        'T10Y3M': '10Y_3M',
        'DGS30': '30_Year',
        'DGS10': '10_Year',
        'DGS2': '2_Year',
        'DGS3MO': '3_Month',
    }
    frequency: Frequency = Frequency.DAILY
    data: DataType = DataType.INDEX
    stats: StatsType = StatsType.DIFFERENCE
