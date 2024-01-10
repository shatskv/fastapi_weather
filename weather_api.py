from typing import Union

from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException
import os

app = FastAPI()
import requests
from requests import HTTPError, ConnectionError

load_dotenv()

@app.get("/weather/")
def read_root(request: Request, city: str):
    api_id = os.getenv('APP_ID')
    url = 'https://api.openweathermap.org/data/2.5/weather'
    params = {'q': city,
              'units': 'metric', 
              'appid': api_id}
    try:
        response = requests.get(url, params=params, timeout=(7, 7))
        answer = response.json()
        response.raise_for_status()
    except ConnectionError as e:
        answer = {'error': 'openweather server is not responding', 
                  'url': url}
        raise HTTPException(status_code=502, detail=answer)
    except HTTPError as e:
        answer = {'message': answer.get('message'),
                  'error': str(e),
                  'code': response.status_code}
        raise HTTPException(status_code=response.status_code, detail=answer)
    else:
        temp = answer.get('main', {}).get('temp')
        temp = round(temp, 1) if temp else None
        city = city.capitalize() if city else None
        answer = {'city': city,
                  'temperature': temp,
                  'units': 'celsius'
                  }
    return answer


if __name__ == '__main__':
    load_dotenv()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
