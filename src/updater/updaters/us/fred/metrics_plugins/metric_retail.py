from updaters.us.interfaces import UsMetric, Frequency, DataType, StatsType


class Metric(UsMetric):
    code: str = 'retail'
    name: str = 'Retail Sales'
    constituents: dict[str, str] = {
        'RSAFS': 'Retail Sales',
        'RSFSXMV': 'ex Auto',
        'MARTSSM44W72USS': 'Core',
        'RSMVPD': 'Motor Vehicle',
        'RSNSR': 'Non Store',
        'RSDBS': 'Food and Beverage',
        'RSFSDP': 'Food Services',
        'RSGMS': 'General Merchandise',
        'RSGASS': 'Gas Stations',
        'RSBMGESD': 'Housing Supplies',
        'RSHPCS': 'Health Care',
        'RSCCAS': 'Clothing',
        'RSFHFS': 'Furniture',
        'RSEAS': 'Electronics and Appliences',
        'RSMSR': 'Miscellaneous stores',
        'RSSGHBMS': 'Sporting Hobby Books Music',
    }
    frequency: Frequency = Frequency.MONTHLY
    data: DataType = DataType.CHANGE
    stats: StatsType = StatsType.DIFFERENCE
    