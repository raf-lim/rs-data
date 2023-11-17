from updaters.us.index import main_us
from updaters.eu.index import main_eu
from updaters.libs import exceptions


if __name__ == "__main__":
    try:
        main_us()
    except exceptions.MissingFredApiKeyException:
        pass

    main_eu()

