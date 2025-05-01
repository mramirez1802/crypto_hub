import unittest
from unittest.mock import patch, MagicMock
from database.data_processor import DataBaseManager


class TestDataBaseManager(unittest.TestCase):
    """Unit tests for MySQL database operations."""

    def setUp(self):
        """Initialize the database manager instance."""
        self.db_manager = DataBaseManager()

    @patch("database.data_processor.connector.connect")
    def test_database_connection(self, mock_connect):
        """Test successful database connection."""
        mock_connection = MagicMock()
        mock_connection.is_connected.return_value = True
        mock_connect.return_value = mock_connection

        self.db_manager.connect()
        self.assertIsNotNone(self.db_manager.connection)
        self.assertTrue(self.db_manager.connection.is_connected())

    @patch("database.data_processor.DataBaseManager.read_schema_config")
    @patch("database.data_processor.connector.connect")
    def test_truncate_tables(self, mock_connect, mock_read_schema):
        """Test truncating tables based on schema configuration."""
        mock_connection = MagicMock()
        mock_connection.is_connected.return_value = True
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection
        mock_read_schema.return_value = [{"name": "test_table"}]

        self.db_manager.connect()
        self.db_manager.truncate_tables()
        mock_cursor.execute.assert_called_with("TRUNCATE TABLE test_table;")


if __name__ == "__main__":
    unittest.main()
