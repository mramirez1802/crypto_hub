from config.settings import DATABASE, SCHEMA_CONFIG_PATH
from mysql import connector
import json


class DataBaseManager:
    """Class to manage MySQL database connection and operations."""

    def __init__(self):
        """Initialize database parameters and connections."""
        self.database_params = DATABASE
        self.schema_path = SCHEMA_CONFIG_PATH
        self.connection = None
        self.cursor = None

    def connect(self):
        """Establish connection to the database."""
        try:
            self.connection = connector.connect(**self.database_params)
            if self.connection.is_connected():
                self.cursor = self.connection.cursor()
                print("Successfully connected to the database")
        except connector.Error as err:
            print(f"Database connection error: {err}")
            self.connection = None

    def read_schema_config(self):
        """Read and parse the JSON schema configuration file."""
        try:
            with open(self.schema_path, 'r', encoding='utf-8') as file:
                return json.load(file).get("tables", [])
        except (FileNotFoundError, json.JSONDecodeError) as err:
            print(f"Error reading schema config: {err}")
            return None

    def truncate_tables(self):
        """Truncate all tables listed in the schema configuration."""
        db_properties = self.read_schema_config()
        if not db_properties:
            print("Failed to read schema config")
            return

        if not self.is_connected():
            print("No active database connection")
            return

        for table in (t['name'] for t in db_properties):
            try:
                self.cursor.execute(f"TRUNCATE TABLE {table};")
                print(f"Table '{table}' truncated successfully")
            except connector.Error as err:
                error_map = {
                    1146: f"Error: Table '{table}' does not exist.",
                    1044: f"Error: No permission to truncate '{table}'.",
                    2003: "Error: Connection issue with MySQL."
                }

                print(error_map.get(err.errno, f"Unexpected error on '{table}': {err}"))

    def insert_data(self, data):
        """Insert data into tables as per the schema configuration."""
        db_properties = self.read_schema_config()
        if not db_properties:
            print("Failed to read schema config")
            return

        if not self.is_connected():
            print("No active database connection")
            return

        table_map = {t['name']: t for t in db_properties}

        # Insert crypto data
        if "cryptos" in table_map:
            cryptos_table = table_map["cryptos"]
            values = [(coin['id'], coin['symbol'], coin['name']) for coin in data['coins_data']
                      if all(str(value).isalnum() for key, value in coin.items() if key in cryptos_table['columns'])]
            self._execute_insert(cryptos_table, values)

        # Insert market bitcoin data
        if "market_bitcoin" in table_map:
            market_table = table_map["market_bitcoin"]
            bitcoin_id = data['bitcoin_market_data']['id']
            market_prices = [(cur, price) for cur, price in
                             data['bitcoin_market_data']['market_data']['current_price'].items()]
            market_caps = list(data['bitcoin_market_data']['market_data']['market_cap'].values())
            total_volumes = list(data['bitcoin_market_data']['market_data']['total_volume'].values())

            values = [(bitcoin_id, cur, int(price),
                       int(market_caps[i] if i < len(market_caps) and market_caps[i] is not None else 0),
                       int(total_volumes[i] if i < len(total_volumes) and total_volumes[i] is not None else 0))
                      for i, (cur, price) in enumerate(market_prices)]
            self._execute_insert(market_table, values)

        # Insert historical bitcoin prices data
        if "historical_bitcoin_prices" in table_map:
            historical_bitcoin_prices_table = table_map["historical_bitcoin_prices"]
            historic_prices = [(t_unix, price) for t_unix, price in data["historical_bitcoin_prices_data"]["prices"]]
            historic_market_caps = [(t_unix, market_cap) for t_unix, market_cap in
                                    data["historical_bitcoin_prices_data"]["market_caps"]]
            historic_market_total_volume = [(t_unix, total_volume) for t_unix, total_volume in
                                            data["historical_bitcoin_prices_data"]["total_volumes"]]

            values = [
                (t_unix, float(price), float(market_cap), float(total_volume))
                for (t_unix, price), (_, market_cap), (_, total_volume)
                in zip(historic_prices, historic_market_caps, historic_market_total_volume)
            ]

            self._execute_insert(historical_bitcoin_prices_table, values)

    def _execute_insert(self, table, values):
        """Helper method to execute insert query."""
        try:
            query = (f"INSERT INTO {table['name']} ({', '.join(table['columns'])}) "
                     f"VALUES ({', '.join(['%s'] * len(table['columns']))})")
            self.cursor.executemany(query, values)
            self.connection.commit()
            print(f"Data inserted into '{table['name']}' successfully")
        except connector.Error as err:
            print(f"Error inserting into '{table['name']}': {err}")

    def is_connected(self):
        """Check if the database connection is active."""
        return self.connection and self.connection.is_connected()

    def close(self):
        """Close the database connection and cursor."""
        if self.cursor:
            self.cursor.close()
        if self.is_connected():
            self.connection.close()
            print("Database connection closed")
