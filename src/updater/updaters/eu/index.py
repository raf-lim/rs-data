from os import getenv
import logging
from requests import HTTPError
import pandas as pd
from db.base import engine
from updaters.libs import cleaners, statistics
from updaters.eu import countries, metrics, collectors


def main_eu():
    """Main function for EU updater."""
    
    BASE_URL = getenv("EUROSTAT_BASE_URL")
    MONTHS_LIMIT = int(getenv("EU_DATA_MONTHS_LIMIT"))

    # countries_metrics_data: dict[str, pd.DataFrame] = {}
    for metric in metrics.esi_metrics:
        
        countries_metric: list[pd.DataFrame] = []
        for country_code in countries.eu_countries:
            
            url = collectors.compile_endpoint_url(
                BASE_URL, country_code, metric.code,
                )
            try:
                data = collectors.get_data(url)
            except HTTPError as e:
                logging.warning(
                    f"{metric.name} for {country_code} error, message: {e}"
                    )
                continue

            country_metric_data = (
                collectors.parse_country_metric_data(data)[-MONTHS_LIMIT:]
                )
            country_metric_data.rename(
                columns={
                    country_metric_data.columns[0]: 
                    f"{country_code}-{metric.name}",
                    },
                inplace=True,
                )
            countries_metric.append(country_metric_data)

        countries_metric_data_table = (
            pd.concat(countries_metric, axis=1).sort_index()
            )
        # Clean constituents series recently not reported.
        # and convert into percentage change series if relevant.  
        countries_metric_data_table = cleaners.remove_longer_not_reported(
            data=countries_metric_data_table, last_not_reported=6,
            )
        # countries_metrics_data[metric.name] = countries_metric_data_table

        stats = pd.DataFrame()
        for country in countries_metric_data_table.columns:
            data = countries_metric_data_table[country]
            stats_data = statistics.compute_statistics_difference(
                data, year_readings_number=12,
                )
            stats_data.name = country
            stats = pd.concat([stats, stats_data], axis=1)

        # Save metric tables in database
        with engine.connect() as conn:
            
            try:
                countries_metric_data_table.to_sql(
                    name=f"eu_metric_{metric.name.lower()}_data",
                    con=conn,
                    if_exists="replace",
                    index=True,
                    )
            except KeyError as e:
                logging.warning(f"KeyError: {e}")
            
            try:
                stats.to_sql(
                    name=f"eu_metric_{metric.name.lower()}_stats",
                    con=conn,
                    if_exists="replace",
                    index=True,
                    )
            except KeyError as e:
                logging.warning(f"KeyError: {e}")

            conn.commit()
