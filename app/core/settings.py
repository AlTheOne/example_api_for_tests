import os
from pathlib import Path

from starlette.config import Config


config = Config('.env')

# Dir...
ROOT_DIR = os.path.dirname(Path(__file__).parents[0])
STATIC_DIR = f'{ROOT_DIR}/statics' if ROOT_DIR else 'statics'
if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR)

# Database...
DB_URL: str = config('DB_URL', default='sqlite:///test.db')

# Framework...
API_PREFIX = '/api'
VERSION = '0.0.1'
DEBUG: bool = config('DEBUG', cast=bool, default=False)
PROJECT_NAME: str = config('PROJECT_NAME', default='Test AlTheOne APP')

# Auth...
JWT_SECRET_KEY: str = config('JWT_SECRET_KEY', cast=str, default='SECRET')
JWT_ALGORITHM: str = 'HS256'
JWT_PREFIX_TOKEN = 'JWT'
JWT_ACCESS_SUBJECT = 'ACCESS'
JWT_REFRESH_SUBJECT = 'REFRESH'
