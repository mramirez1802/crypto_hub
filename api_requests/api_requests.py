from requests import get, HTTPError, ConnectionError, Timeout, RequestException
from urllib.parse import urlencode
from config.settings import COINGECKO
import time


class APICoinGecko:
    """Class to handle the CoinGecko API with caching and error management"""

    def __init__(self):
        """Initialize connection parameters with CoinGecko"""
        self.base_url = COINGECKO['api_url_token']
        self.endpoints = {
            'list': 'coins/list',
            'market_chart': 'coins/{coin_id}/market_chart/range'
        }
        self.market_data = COINGECKO['market_data']
        self.currency = COINGECKO['currency']
        self.start_date = COINGECKO['from_timestamp']
        self.end_date = COINGECKO['to_timestamp']
        self.headers = {"Authorization": f"Bearer {COINGECKO['api_token']}"}
        self.coins_cache = None  # Now using `self.coins_cache` instead of `self.all_coins`

    def get_all_coins(self):
        """Fetch API data if no cached data is available"""
        if self.coins_cache is None:
            url = f"{self.base_url}/{self.endpoints['list']}"
            print(f'Fetching: {url}')
            response = self._make_request(url)
            if response:
                self.coins_cache = response  # Store data in memory
        return self.coins_cache

    def get_cached_coins(self):
        """Return cached data without making a new request"""
        if self.coins_cache is None:
            print("No cached data available. Running `get_all_coins()`...")
            return self.get_all_coins()  # Fetch from API if not loaded
        return self.coins_cache  # Return stored data

    def get_market_bitcoin_details(self):
        """Retrieve Bitcoin market details using cached crypto data"""

        # Use cached crypto data instead of making a new API request
        parsed_result = self.get_cached_coins()

        if not parsed_result:
            print("Could not fetch the crypto list.")
            return None

        # Search for Bitcoin in the crypto list
        coin = next((i for i in parsed_result if i['id'] == 'bitcoin'), None)

        if not coin:
            print("Bitcoin not found in the crypto list.")
            return None

        # Construct query parameters
        query_params = {'market_data': self.market_data}

        # Build the complete URL
        url = f"{self.base_url}/coins/{coin['id']}?{urlencode(query_params)}"
        print(f'Fetching: {url}')

        return self._make_request(url)

    def get_historical_bitcoin_prices(self):
        """Retrieve historical Bitcoin prices"""
        parsed_result = self.get_cached_coins()
        if not parsed_result:
            print("Could not fetch the crypto list.")
            return None

        coin = next((i for i in parsed_result if i['id'] == 'bitcoin'), None)
        if not coin:
            print("Bitcoin not found in the crypto list.")
            return None

        query_params = {
            'vs_currency': self.currency,
            'from': self.start_date,
            'to': self.end_date
        }

        url = f"{self.base_url}/coins/{coin['id']}/market_chart/range?{urlencode(query_params)}"
        print(f'Fetching: {url}')

        return self._make_request(url)

    def _make_request(self, url, retries=3):
        """Method to handle requests with retries in case of a 429 error"""
        for attempt in range(retries):
            try:
                response = get(url, headers=self.headers, timeout=10)
                response.raise_for_status()

                if response.status_code == 429:
                    print(f"Request limit reached, retrying in 10s... (Attempt {attempt + 1})")
                    time.sleep(10)
                    continue  # Retry request

                return response.json()

            except (HTTPError, ConnectionError, Timeout, RequestException) as err:
                print(f'Request error: {err}')
            except Exception as err:
                print(f'Unknown error: {err}')

        print("Error after multiple attempts.")
        return None
