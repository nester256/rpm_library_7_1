from requests import get
from . import config


def get_weather(location: str):
    params = config.LOCATIONS_COORDINATES.get(location)
    if params:
        return get(
            config.YANDEX_API_URL,
            params=params,
            headers={
                config.YANDEX_API_HEADER: config.YANDEX_KEY
            }
        )
    return None
