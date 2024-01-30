from typing import Optional

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, ValidationError
from requests import ConnectionError, HTTPError

from weather.config import load_from_env
from weather.openweather import fetch_weather

app = FastAPI()


class Weather(BaseModel):
    city: str


class Main(BaseModel):
    temp: float
    feels_like: float
    temp_min: float
    temp_max: float
    pressure: float
    humidity: int
    sea_level: Optional[int] = None
    grnd_level: Optional[int] = None


class WeatherResponse(BaseModel):
    coord: dict
    weather: list
    base: str
    main: Main
    visibility: int
    wind: dict
    clouds: dict
    dt: int
    sys: dict
    timezone: int
    id: int
    name: str
    cod: int


@app.get("/weather/")
def read_root(request: Request, city: str):
    api_config = load_from_env()
    try:
        weather = Weather(city=city)
    except ValidationError as e:
        answer = {'error': {'message': e.json(), 'code': 'validation_error' }}
        raise HTTPException(status_code=400, detail=answer)
    try:
        response = fetch_weather(weather.city, api_config)
        response.raise_for_status()
    except ConnectionError as e:
        answer = {'error': {'message': 'openweather server is not responding', 'code': 'connection_error' }}
        raise HTTPException(status_code=502, detail=answer)
    except HTTPError as e:
        answer = {'error': {'message': response.json().get('message'),
                  'detail': str(e),
                  'code': 'http_error'}}
        raise HTTPException(status_code=response.status_code, detail=answer)
    else:
        answer = response.json()
        try:
            weather_response = WeatherResponse(**answer)
        except ValidationError as e:
            answer = {'error': {'message': e.json(), 'code': 'response_validation_error' }}
            raise HTTPException(status_code=500, detail=answer)

        temp = weather_response.main.temp
        city = weather_response.name
        answer = {'city': city,
                  'temperature': temp,
                  'units': 'celsius'
                  }
    return answer


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
