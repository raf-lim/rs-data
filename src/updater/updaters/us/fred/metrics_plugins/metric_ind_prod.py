from updaters.us.interfaces import UsMetric, Frequency, DataType, StatsType


class Metric(UsMetric):
    code: str = 'ind_prod'
    name: str = 'Industrial Production'
    constituents: dict[str, str] = {
        'INDPRO': 'Industrial Production',
        'IPCONGD': 'Consumer Goods',
        'IPBUSEQ': 'Business Equipment',
        'IPB54100S': 'Construction',
        'IPMAT': 'Materials',
        'IPMAN': 'Manufacturing',
        'IPMINE': 'Mining',
        'IPUTIL': 'Utilities',
        'TCU': 'Capacity Utilization',
    }
    frequency: Frequency = Frequency.MONTHLY
    data: DataType = DataType.CHANGE
    stats: StatsType = StatsType.DIFFERENCE
