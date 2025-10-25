import unittest
from unittest.mock import patch, MagicMock
from psycopg import OperationalError
from astera.services.database.db_utils import connect_to_db, create_tables


class TestDbUtils(unittest.TestCase):

    @patch('astera.services.database.db_utils.psycopg')
    def test_connect_success(self, mock_psycopg):

        expected_connect = MagicMock()
        mock_psycopg.connect.return_value = expected_connect
        actual_connect = connect_to_db()
        mock_psycopg.connect.assert_called_once()
        self.assertEqual(actual_connect, expected_connect)

    @patch("astera.services.database.db_utils.psycopg")
    def test_failue_connect(self, mock_psycopg):
        mock_psycopg.connect.side_effect = OperationalError
        actual_connect = connect_to_db()
        self.assertIsNone(actual_connect)
        mock_psycopg.connect.assert_called_once()

    def test_create_tables_success(self):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        create_tables(mock_connection)

        self.assertEqual(mock_cursor.execute.call_count, 3)
        mock_connection.commit.assert_called_once()
        mock_connection.rollback.assert_not_called()
    
    def test_create_tables_failure(self):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.execute.side_effect = Exception("Simulated DB error")
        create_tables(mock_connection)
        mock_connection.commit.assert_not_called()
        mock_connection.rollback.assert_called_once()


if __name__ == "__main__":
    unittest.main()
