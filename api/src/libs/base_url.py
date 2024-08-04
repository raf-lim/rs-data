from os import getenv


def get_base_api_url() -> str:
    """Returns base api url"""
    return getenv("THIS_API_BASE_URL")
