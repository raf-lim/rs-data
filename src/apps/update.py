import logging
from db.base import engine
from updater.us.fred import metrics
from updater.us.fred import collectors



if __name__ == "__main__":

    with engine.connect() as connection:
        for metric in metrics.metrics:
            try:
                data = collectors.get_together_constituents_data(
                    metric=metric,
                    data_getter=collectors.get_constituent_data
                )
                data.to_sql(metric.name.lower(), connection, if_exists="replace")
            except Exception as e:
                logging.warning(e)
                continue

            #TODO: continue with add statistics.
            print(data)
            # data.to_sql(metric.name, connection, if_exists="replace")
        
        # connection.commit()