import unittest
from unittest.mock import MagicMock, patch
from astera.services.user_manager import create_user


class TestUserManager(unittest.TestCase):

    @patch("astera.services.user_manager.connect_to_db")
    def test_create_user_success(self, mock_connect_to_db):
        mock_connect = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.__enter__.return_value = mock_cursor

        mock_connect.cursor.return_value = mock_cursor
        mock_connect_to_db.return_value = mock_connect

        test_user_name = "Test_user"
        create_user(test_user_name)

        mock_connect_to_db.assert_called_once()
        mock_connect.cursor.assert_called_once()

        expected_sql = "INSERT INTO users(user_name) VALUES(%s)"
        expected_params = (test_user_name,)
        mock_cursor.execute.assert_called_once_with(expected_sql, expected_params)
        mock_connect.commit.assert_called_once()
        mock_connect.close.assert_called_once()

    @patch("astera.services.user_manager.connect_to_db")
    def test_create_user_connection_failur(self, mock_connect_to_db):
        mock_connect_to_db.return_value = None
        result = create_user("No DB User")

        self.assertIsNone(result, "Must be return None ")
        mock_connect_to_db.assert_called_once()

    @patch("astera.services.user_manager.connect_to_db")
    def test_create_user_rollback_on_error(self, mock_connect_to_db):
        mock_connect = MagicMock()
        mock_cursor = MagicMock()

        mock_cursor.__enter__.return_value = mock_cursor
        mock_connect.cursor.return_value = mock_cursor
        mock_connect_to_db.return_value = mock_connect

        mock_cursor.execute.side_effect = Exception("Simulated DB error")
        create_user("Error_User")

        mock_connect.rollback.assert_called_once()
        mock_connect.close.assert_called_once()
        mock_connect.commit.assert_not_called()
        mock_cursor.execute.assert_called_once()
