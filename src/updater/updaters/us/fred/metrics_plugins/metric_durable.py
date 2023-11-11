from updaters.us.interfaces import UsMetric, Frequency, DataType, StatsType


class Metric(UsMetric):
    code: str = 'durable'
    name: str = 'New Orders of Durable Goods'
    constituents: dict[str, str] = {
        'DGORDER': 'New Orders',
        'ADXTNO': 'ex Transport',
        'NEWORDER': 'Core',
        'AMTUNO': 'Manufacturing',
        'A36SNO': 'Transportation Equipment',
        'A32SNO': 'Fabricated Metal Products',
        'A33SNO': 'Machinery',
        'A34SNO': 'Computers',
        'A31SNO': 'Primary Metals',
        'A35SNO': 'Electrical Equipment',
    }
    frequency: Frequency = Frequency.MONTHLY
    data: DataType = DataType.CHANGE
    stats: StatsType = StatsType.DIFFERENCE
    