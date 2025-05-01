from decouple import config
from os import path

# ===========================
# General configuration
# ===========================
PROJECT_NAME = 'Crypto Hub'
VERSION = '1.0.0'
AUTHOR = 'Manuel Ramirez Monroy'
DEBUG = config('DEBUG', default=True, cast=bool)

# ===========================
# Database configuration
# ===========================
DATABASE = {
    'database': config('MYSQL_DATABASE'),
    'user': config('MYSQL_USER'),
    'password': config('MYSQL_PASSWORD'),
    'host': config('MYSQL_HOST'),
    'port': config('MYSQL_PORT', cast=int)
}

# ===========================
# CoinGecko API token configuration
# ===========================
COINGECKO = {
    'api_url_token': config('API_URL'),
    'api_token': config('API_TOKEN'),
    'market_data': config('MARKET_DATA', cast=bool),
    'currency': config('CURRENCY'),
    'from_timestamp': config('START_DATE_UNIX'),
    'to_timestamp': config('END_DATE_UNIX')
}

# ===========================
# Column file (JSON)
# ===========================
BASE_DIR = path.abspath(path.dirname(__file__))
CONFIG_DIR = path.join(BASE_DIR, '..\\config')  # Configuration directory
SCHEMA_CONFIG_PATH = path.join(CONFIG_DIR, 'schema.json')

# ===========================
# Logging configuration
# ===========================
LOG_LEVEL = config('LOG_LEVEL', default='INFO')


# ===========================
# Utility functions
# ===========================
def show_settings():
    """Display current configuration settings"""
    print(f'Project Name: {PROJECT_NAME}')
    print(f'Version: {VERSION}')
    print(f'Author: {AUTHOR}')
    print(f'Debug Mode: {DEBUG}')
    print(f"Database Host: {DATABASE['host']}")
    print(f"API Url Token: {COINGECKO['api_url_token']}")
    print(f"API Token: {COINGECKO['api_token']}")
    print(f"Market Data: {COINGECKO['market_data']}")
    print(f"Parameter Currency: {COINGECKO['currency']}")
    print(f"Parameter from_date: {COINGECKO['from_timestamp']}")
    print(f"Parameter to_date: {COINGECKO['to_timestamp']}")


if __name__ == '__main__':
    show_settings()
