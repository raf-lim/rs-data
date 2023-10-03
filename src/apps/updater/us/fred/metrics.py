# US macroeconomy metrics from FRED.
from us.interfaces import Metric, Frequency, TableType, StatsType


class Gdp:
    code = 'gdp'
    name = 'GDP'
    constituents = {
        'GDPC1': 'Real GDP',
        'PCECC96': 'Consumption',
        'GPDIC1': 'Investments',
        'GCEC1': 'Government',
        'IMPGSC1': 'Imports',
        'EXPGSC1': 'Exports',
    }
    frequency = Frequency.QUARTERLY
    table = (TableType.CHANGE, StatsType.DIFFERENCE)


class GdpPriceIndex:
    code = 'gdp_price_index'
    name = 'GDP Price Index'
    constituents = {
        'GDPCTPI': 'GDP Price Index',
        'JCXFE': 'PCE Core Price Index',
    }
    frequency = Frequency.QUARTERLY
    table = (TableType.CHANGE, StatsType.DIFFERENCE)


class DebtToGdp:
    code = 'debt_gdp'
    name = 'Debt to GDP'
    constituents = {'GFDEGDQ188S': 'Debt to GDP',}
    frequency = Frequency.QUARTERLY
    table = (TableType.CHANGE, StatsType.DIFFERENCE)


class EmploymentCostIndex:
    code = 'empl_cost'
    name = 'Employment Cost Index'
    constituents = {'ECIALLCIV': 'Employment Cost Index'}
    frequency = Frequency.QUARTERLY
    table = (TableType.CHANGE, StatsType.DIFFERENCE)


class Inflation:
    code = 'inflation'
    name = 'Inflation'
    constituents = {
        'PCEPI': 'PCE',
        'PCEPILFE': 'Core PCE',
        'CPIAUCSL': 'CPI',
        'CPILFESL': 'Core CPI',
        'CPIFABSL': 'Food CPI',
        'CPIENGSL': 'Energy CPI',
        'PPICOR': 'PPI Core',
    }
    frequency = Frequency.MONTHLY
    table = (TableType.CHANGE, StatsType.DIFFERENCE)


class RetailSales:
    code = 'retail'
    name = 'Retail Sales'
    constituents = {
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
    frequency = Frequency.MONTHLY
    table = (TableType.CHANGE, StatsType.DIFFERENCE)


class IndustrialProduction:
    code = 'ind_prod'
    name = 'Industrial Production'
    constituents = {
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
    frequency = Frequency.MONTHLY
    table = (TableType.CHANGE, StatsType.DIFFERENCE)


class DurableGoods:
    code = 'durable'
    name = 'New Orders of Durable Goods'
    constituents = {
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
    frequency = Frequency.MONTHLY
    table = (TableType.CHANGE, StatsType.DIFFERENCE)


class Housing:
    code = 'housing'
    name = 'Housing'
    constituents = {
        'PERMIT': 'Permits',
        'HOUST': 'Started',
        'COMPUTSA': 'Completed',
        }
    frequency = Frequency.MONTHLY
    table = (TableType.INDEX, StatsType.CHANGE)


class JobsNfp:
    code = 'jobs_nfp'
    name = 'Jobs'
    constituents = {
        'PAYEMS': 'NFP',
        'CES0500000011': 'Weekly Earnings'
        }
    frequency = Frequency.MONTHLY
    table = (TableType.INDEX, StatsType.DIFFERENCE)


class JobsUr:
    code = 'jobs_ur'
    name = 'Jobs'
    constituents = {
        'UNRATE': 'UR',
        'CIVPART': 'Participation Rate'
        }
    frequency = Frequency.MONTHLY
    table = (TableType.INDEX, StatsType.DIFFERENCE)


class FedFunds:
    code = 'fed'
    name = 'FED Funds Rate'
    constituents = {'FEDFUNDS': 'FED Funds'}
    frequency = Frequency.MONTHLY
    table = (TableType.INDEX, StatsType.DIFFERENCE)


class TradeBalance:
    code = 'trade'
    name = 'Trade Balance'
    constituents = {'BOPGSTB': 'Trade Balance'}
    frequency = Frequency.MONTHLY
    table = table = (TableType.INDEX, StatsType.CHANGE)


class JoblessClaims:
    code = 'claims'
    name = 'Jobless Claims'
    constituents = {
        'ICSA': 'Initial Claims',
        'CCSA': 'Continued Claims',
        }
    frequency = Frequency.WEEKLY
    table = (TableType.INDEX, StatsType.DIFFERENCE)


class MoneyStock:
    code = 'money'
    name = 'Money Stock'
    constituents = {
        'WM1NS': 'M1',
        'WM2NS': 'M2',
        }
    frequency = Frequency.WEEKLY
    table = (TableType.CHANGE, StatsType.DIFFERENCE)


class TotalAssets:
    code = 'assets'
    name = 'Total Assets'
    constituents = {'WALCL': 'Total Assets',}
    frequency = Frequency.WEEKLY
    table = (TableType.CHANGE, StatsType.DIFFERENCE)


class BondYields:
    code = 'yields'
    name = 'Bond Yields'
    constituents = {
        'T10Y2Y': '10Y_2Y',
        'T10Y3M': '10Y_3M',
        'DGS30': '30_Year',
        'DGS10': '10_Year',
        'DGS2': '2_Year',
        'DGS3MO': '3_Month',
    }
    frequency = Frequency.DAILY
    table = (TableType.INDEX, StatsType.DIFFERENCE)


metrics: list[Metric] = [
    Housing,
    RetailSales,
    IndustrialProduction,
    DurableGoods,
    JoblessClaims,
    JobsNfp,
    JobsUr,
    EmploymentCostIndex,
    Inflation,
    Gdp,
    GdpPriceIndex,
    TradeBalance,
    DebtToGdp,
    TotalAssets,
    FedFunds,
    BondYields,
    MoneyStock,
]
