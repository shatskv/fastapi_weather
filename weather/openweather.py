import requests

from weather.config import ApiConfig


def fetch_weather(city, api_config: ApiConfig):
    api_id = api_config.api_key
    url = 'https://api.openweathermap.org/data/2.5/weather'
    params = {'q': city,
            'units': 'metric', 
            'appid': api_id}
    response = requests.get(url, params=params, timeout=(7, 7))
    return response
