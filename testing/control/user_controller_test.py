"""User Test Suite"""
import unittest
from unittest.mock import MagicMock, patch

# Replace 'control.user_controller' with the actual import path
from control.user_controller import UserController


class TestUserController(unittest.TestCase):
    """User Test Suite """
    @patch("control.user_controller.MongoDBConnection")
    def setUp(self, mock_db_conn_class): # pylint: disable=arguments-differ
        """Runs before each test method.

        Sets up a mock database collection table for 'users'.
        """
        self.mock_table = MagicMock()
        mock_db_conn_class.return_value.get_table.return_value = self.mock_table

        self.controller = UserController()
        mock_db_conn_class.assert_called_once_with("users")

    # -------------------------------------------------------------------------
    # Tests for create_or_retrieve_user
    # -------------------------------------------------------------------------

    def test_create_or_retrieve_user_creates_new_user_when_not_exists(self):
        """Validate empty string on user does not exist"""
        # Arrange: User does not exist (count == 0)
        self.mock_table.count_documents.return_value = 0
        user_payload = {
            "auth_id": "auth0|12345",
            "username": "johndoe",
            "email": "john@example.com",
        }
        self.mock_table.find_one.return_value = user_payload

        # Act
        result = self.controller.create_or_retrieve_user(user_payload)

        # Assert
        self.mock_table.count_documents.assert_called_once_with(
            {"auth_id": "auth0|12345"}
        )
        self.mock_table.insert_one.assert_called_once_with(user_payload)
        self.mock_table.find_one.assert_called_once_with(
            {"auth_id": "auth0|12345"}
        )
        self.assertEqual(result, user_payload)

    def test_create_or_retrieve_user_returns_existing_without_insert(self):
        """Validate the create if not existing"""
        # Arrange: User already exists (count == 1)
        self.mock_table.count_documents.return_value = 1
        user_payload = {
            "auth_id": "auth0|12345",
            "username": "johndoe",
            "email": "john@example.com",
        }
        self.mock_table.find_one.return_value = user_payload

        # Act
        result = self.controller.create_or_retrieve_user(user_payload)

        # Assert
        self.mock_table.count_documents.assert_called_once_with(
            {"auth_id": "auth0|12345"}
        )
        self.mock_table.insert_one.assert_not_called()
        self.mock_table.find_one.assert_called_once_with(
            {"auth_id": "auth0|12345"}
        )
        self.assertEqual(result, user_payload)

    # -------------------------------------------------------------------------
    # Tests for update_username
    # -------------------------------------------------------------------------

    def test_update_username_success(self):
        """Update username test"""
        # Arrange
        user_id = "auth0|12345"
        new_username = "janedoe"
        expected_updated_user = {
            "auth_id": user_id,
            "username": new_username,
            "email": "jane@example.com",
        }
        self.mock_table.find_one.return_value = expected_updated_user

        # Act
        result = self.controller.update_username(user_id, new_username)

        # Assert
        self.mock_table.update_one.assert_called_once_with(
            {"auth_id": user_id}, {"$set": {"username": new_username}}
        )
        self.mock_table.find_one.assert_called_once_with({"auth_id": user_id})
        self.assertEqual(result, expected_updated_user)

    # -------------------------------------------------------------------------
    # Tests for get_user
    # -------------------------------------------------------------------------

    def test_get_user_returns_set_of_username_and_email(self):
        """Validate the retrieve user"""
        # Arrange
        db_user_doc = {
            "_id": "123",
            "username": "johndoe",
            "email": "john@example.com",
            "auth_id": "auth0|12345",
        }
        self.mock_table.find_one.return_value = db_user_doc

        # Act
        result = self.controller.get_user("johndoe")

        # Assert
        self.mock_table.find_one.assert_called_once_with({"username": "johndoe"})
        # Note: The controller returns a set `{user["username"], user["email"]}`
        self.assertEqual(result, {"johndoe", "john@example.com"})

    # -------------------------------------------------------------------------
    # Tests for get_users
    # -------------------------------------------------------------------------

    def test_get_users_returns_list_of_users(self):
        """Validate we return a list of users"""
        # Arrange
        mock_user_list = [
            {"username": "user1", "email": "user1@example.com"},
            {"username": "user2", "email": "user2@example.com"},
        ]
        self.mock_table.find.return_value = mock_user_list

        # Act
        result = self.controller.get_users()

        # Assert
        self.mock_table.find.assert_called_once()
        self.assertEqual(result, mock_user_list)

    # -------------------------------------------------------------------------
    # Tests for login
    # -------------------------------------------------------------------------

    def test_login_returns_true_when_matched_by_username(self):
        # Arrange: Username match count == 1
        self.mock_table.count_documents.return_value = 1

        # Act
        result = self.controller.login("johndoe", "http://pic.url/1.png")

        # Assert
        self.mock_table.count_documents.assert_called_once_with(
            {"username": "johndoe", "picture": "http://pic.url/1.png"}
        )
        self.assertTrue(result)

    def test_login_falls_back_to_email_and_returns_true(self):
        # Arrange: Username match count == 0, Email match count == 1
        self.mock_table.count_documents.side_effect = [0, 1]

        # Act
        result = self.controller.login("john@example.com", "http://pic.url/1.png")

        # Assert
        self.assertEqual(self.mock_table.count_documents.call_count, 2)
        self.mock_table.count_documents.assert_any_call(
            {"username": "john@example.com", "picture": "http://pic.url/1.png"}
        )
        self.mock_table.count_documents.assert_any_call(
            {"email": "john@example.com", "picture": "http://pic.url/1.png"}
        )
        self.assertTrue(result)

    def test_login_returns_false_when_no_match(self):
        """Validate failed login"""
        # Arrange: Username match count == 0, Email match count == 0
        self.mock_table.count_documents.side_effect = [0, 0]

        # Act
        result = self.controller.login("unknown_user", "http://pic.url/1.png")

        # Assert
        self.assertFalse(result)