import logging
from updaters.us.index import main_us
from updaters.eu.index import main_eu
from updaters.dbmf.index import main_dbmf
from updaters.libs import exceptions


if __name__ == "__main__":

    try:
        main_us()
    except exceptions.MissingFredBaseUrlException as e:
        logging.error(e)
    except exceptions.MissingFredApiKeyException as e:
        logging.error(e)
    except exceptions.FredMetricPluginNotFoundException as e: 
        logging.error(e)
    except exceptions.FredMetricsPluginsFolderEmpty as e:
        logging.error(e)
        
    main_eu()

    #main_dbmf()