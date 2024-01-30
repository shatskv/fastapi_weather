from fastapi.testclient import TestClient

from weather.server import app
import pytest

client = TestClient(app)

@pytest.mark.parametrize(
        'city',
        [
            ('London'),
            ('Щелково')
        ]
)
def test__read_root__successful_response(city):
    response = client.get('/weather/', params={'city': city})
    answer = response.json()

    temperature = answer.get('temperature')
    assert response.status_code == 200
    assert answer.get('city') == city
    assert type(temperature) == float
    assert temperature > -100 and temperature < 100
    assert answer.get('units') == 'celsius'


def test__read_root__city_not_found():
    city = 'Щелков44545о'

    response = client.get('/weather/', params={'city': city})
    answer = response.json()

    assert response.status_code == 404
    assert answer == {
        "detail": {
            "error": {
                "message": "city not found",
                "detail": "404 Client Error: Not Found for url: https://api.openweathermap.org/data/2.5/weather?q=%D0%A9%D0%B5%D0%BB%D0%BA%D0%BE%D0%B244545%D0%BE&units=metric&appid=9c9a2588deb7c091073b614032cbaf47",
                "code": "http_error"
            }
        }
    }

def test__read_root__no_city_in_params_get_422():
    response = client.get('/weather/')
    answer = response.json()

    assert response.status_code == 422
    assert answer == {
        "detail": [
            {
                "type": "missing",
                "loc": [
                    "query",
                    "city"
                ],
                "msg": "Field required",
                "input": None,
                "url": "https://errors.pydantic.dev/2.5/v/missing"
            }
        ]
    }
