import os
import logging
from requests import HTTPError
import pandas as pd
from db.base import engine

from updaters.eu import countries, metrics, collectors


def main_eu():
    """Main function for EU updater."""
    BASE_URL = os.getenv("EUROSTAT_BASE_URL")
    MONTHS_LIMIT = int(os.getenv("EU_DATA_MONTHS_LIMIT"))

    countries_metric_tables: dict[str, pd.DataFrame] = {}
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

            country_metric = (
                collectors.parse_country_metric_data(data)[-MONTHS_LIMIT:]
                )
            country_metric.rename(
                columns={
                    country_metric.columns[0]: f"{country_code}-{metric.name}",
                    },
                inplace=True,
                )
            countries_metric.append(country_metric)

        countries_metric_table = pd.concat(countries_metric, axis=1).sort_index()
        countries_metric_tables[metric.name] = countries_metric_table 


        # Save metric tables in database
        with engine.connect() as conn:
            for metric_name, metric_table in countries_metric_tables.items():
                try:
                    metric_table.to_sql(
                        name=f"eu_metric_{metric_name.lower()}_data",
                        con=conn,
                        if_exists="replace",
                        index=True,
                        )
                except KeyError as e:
                    logging.warning(f"KeyError: {e}")
            
            conn.commit()
