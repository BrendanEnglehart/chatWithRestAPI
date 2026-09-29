"""Category controller Unit test framework"""

import unittest
from unittest.mock import MagicMock, patch
from control.category_controller import CategoryController


class TestCategoryController(unittest.TestCase):
    """Main Test Suite for the Categories"""

    @patch("control.category_controller.MongoDBConnection")
    def setUp(self, mock_db_conn_class):
        """Runs before each test method.

        Sets up a fresh MagicMock for the database table collection.
        """
        # Create a mock collection/table instance
        self.mock_table = MagicMock()

        # Wire up MongoDBConnection("category").get_table() to return our mock_table
        mock_db_conn_class.return_value.get_table.return_value = self.mock_table

        # Instantiate controller (calls __init__ using the patched class)
        self.controller = CategoryController()

        # Verify that the DB connection was requested with table "category"
        mock_db_conn_class.assert_called_once_with("category")

    # -------------------------------------------------------------------------
    # Tests for create_category
    # -------------------------------------------------------------------------

    def test_create_category_returns_false_when_already_exists(self):
        """Test duplicate categories"""
        # Arrange: simulate category already exists (count > 0)
        self.mock_table.count_documents.return_value = 1

        # Act
        result = self.controller.create_category(name="general", joinable=True)

        # Assert
        self.mock_table.count_documents.assert_called_once_with(
            {"name": "general", "joinable": True}
        )
        self.mock_table.insert_one.assert_not_called()
        self.assertFalse(result)

    def test_create_category_success_when_new(self):
        """Test Create Category"""
        # Arrange: simulate category does not exist (count == 0)
        self.mock_table.count_documents.return_value = 0
        expected_category = {
            "_id": "123",
            "name": "tech",
            "joinable": True,
        }
        self.mock_table.find_one.return_value = expected_category

        # Act
        result = self.controller.create_category(name="tech", joinable=True)

        # Assert
        self.mock_table.count_documents.assert_called_once_with(
            {"name": "tech", "joinable": True}
        )
        self.mock_table.insert_one.assert_called_once_with(
            {"name": "tech", "joinable": True}
        )
        self.mock_table.find_one.assert_called_once_with(
            {"name": "tech", "joinable": True}
        )
        self.assertEqual(result, expected_category)

    # -------------------------------------------------------------------------
    # Tests for list_categories
    # -------------------------------------------------------------------------

    def test_list_categories_returns_joinable_items(self):
        """Test List Categories"""
        # Arrange
        mock_categories = [
            {"_id": "1", "name": "general", "joinable": True},
            {"_id": "2", "name": "tech", "joinable": True},
        ]
        self.mock_table.find.return_value = mock_categories

        # Act
        result = self.controller.list_categories()

        # Assert
        self.mock_table.find.assert_called_once_with({"joinable": True})
        self.assertEqual(result, mock_categories)

    # -------------------------------------------------------------------------
    # Tests for find_category
    # -------------------------------------------------------------------------

    def test_find_category_returns_matching_document(self):
        """Test Find again"""
        # Arrange
        expected_category = {"_id": "1", "name": "sports", "joinable": False}
        self.mock_table.find_one.return_value = expected_category

        # Act
        result = self.controller.find_category(name="sports", joinable=False)

        # Assert
        self.mock_table.find_one.assert_called_once_with(
            {"name": "sports", "joinable": False}
        )
        self.assertEqual(result, expected_category)

    # -------------------------------------------------------------------------
    # Tests for general_landing
    # -------------------------------------------------------------------------

    def test_general_landing_returns_existing_general_category(self):
        """Test initial account landing"""
        # Arrange: general category exists
        self.mock_table.count_documents.return_value = 1
        expected_category = {"_id": "1", "name": "general", "joinable": True}
        self.mock_table.find_one.return_value = expected_category

        # Act
        result = self.controller.general_landing()

        # Assert
        self.mock_table.count_documents.assert_called_once_with(
            {"name": "general", "joinable": True}
        )
        self.mock_table.find_one.assert_called_once_with(
            {"name": "general", "joinable": True}
        )
        self.mock_table.insert_one.assert_not_called()
        self.assertEqual(result, expected_category)

    @patch.object(CategoryController, "create_category")
    def test_general_landing_creates_general_when_not_found(self, mock_create_category):
        """Test initial account landing on blank instance"""
        # Arrange: general category does not exist
        self.mock_table.count_documents.return_value = 0
        expected_category = {"_id": "99", "name": "general", "joinable": True}
        mock_create_category.return_value = expected_category

        # Act
        result = self.controller.general_landing()

        # Assert
        self.mock_table.count_documents.assert_called_once_with(
            {"name": "general", "joinable": True}
        )
        mock_create_category.assert_called_once_with("general", True)
        self.assertEqual(result, expected_category)
