from updaters.us.interfaces import UsMetric, Frequency, DataType, StatsType


class Metric(UsMetric):
    code: str = 'inflation'
    name: str = 'Inflation'
    constituents: dict[str, str] = {
        'PCEPI': 'PCE',
        'PCEPILFE': 'Core PCE',
        'CPIAUCSL': 'CPI',
        'CPILFESL': 'Core CPI',
        'CPIFABSL': 'Food CPI',
        'CPIENGSL': 'Energy CPI',
        'PPICOR': 'PPI Core',
    }
    frequency: Frequency = Frequency.MONTHLY
    data: DataType = DataType.CHANGE
    stats: StatsType = StatsType.DIFFERENCE
