from api_requests.api_requests import APICoinGecko
from database.data_processor import DataBaseManager


def main():
    """
    Main function to orchestrate API requests and database operations.
    """

    # Instantiate APICoinGecko class
    coingecko = APICoinGecko()

    # Create the dictionary to store retrieved data
    crypto_data = {
        "coins_data": coingecko.get_cached_coins(),  # Fetch cached cryptocurrency list
        "bitcoin_market_data": coingecko.get_market_bitcoin_details(),  # Get current Bitcoin market data
        "historical_bitcoin_prices_data": coingecko.get_historical_bitcoin_prices()
    }

    # Instantiate DataBaseManager class
    db = DataBaseManager()

    # Establish connection to the database
    db.connect()

    # Truncate tables before inserting new data
    db.truncate_tables()

    # Insert retrieved data into the database
    db.insert_data(data=crypto_data)

    # Close the database connection
    db.close()


if __name__ == '__main__':
    main()
