import unittest
from unittest.mock import patch, MagicMock
from api_requests.api_requests import APICoinGecko


class TestAPICoinGecko(unittest.TestCase):
    """Unit tests for CoinGecko API interactions."""

    def setUp(self):
        """Initialize the API class instance."""
        self.api = APICoinGecko()

    @patch("api_requests.api_requests.get")
    def test_get_all_coins(self, mock_get):
        """Test API response for retrieving all coins."""
        mock_response = MagicMock()
        mock_response.json.return_value = [{"id": "bitcoin", "name": "Bitcoin"}]
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        result = self.api.get_all_coins()
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        self.assertEqual(result[0]["id"], "bitcoin")

    @patch("api_requests.api_requests.get")
    def test_get_market_bitcoin_details(self, mock_get):
        """Test API response for retrieving Bitcoin market data."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": "bitcoin", "market_data": {"current_price": {"usd": 50000}}}
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        # Manually setting the cache to avoid API calls
        self.api.coins_cache = [{"id": "bitcoin", "name": "Bitcoin"}]

        result = self.api.get_market_bitcoin_details()
        self.assertIsInstance(result, dict)
        self.assertEqual(result["id"], "bitcoin")
        self.assertIn("market_data", result)

    @patch("api_requests.api_requests.get")
    def test_get_historical_bitcoin_prices(self, mock_get):
        """Test API response for retrieving historical Bitcoin prices."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "prices": [[1672531200, 50000.0]],
            "market_caps": [[1672531200, 950000000000]],
            "total_volumes": [[1672531200, 35000000000]]
        }
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        # Manually setting the cache to avoid API calls
        self.api.coins_cache = [{"id": "bitcoin", "name": "Bitcoin"}]

        result = self.api.get_historical_bitcoin_prices()
        self.assertIsInstance(result, dict)
        self.assertIn("prices", result)
        self.assertIn("market_caps", result)
        self.assertIn("total_volumes", result)


if __name__ == "__main__":
    unittest.main()
