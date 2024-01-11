import os
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ApiConfig:
    api_key: str


def load_from_env():
    api_key = os.getenv('APP_ID')
    return ApiConfig(api_key)
