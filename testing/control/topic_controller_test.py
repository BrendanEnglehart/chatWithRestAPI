"""Topic Test Suite """
import unittest
from unittest.mock import MagicMock, patch
from bson.objectid import ObjectId

# Replace 'control.topic_controller' with the actual import path
from control.topic_controller import TopicController


class TestTopicController(unittest.TestCase):
    """Topic Test Suite """
    @patch("control.topic_controller.MongoDBConnection")
    #@suppress
    def setUp(self, mock_db_conn_class): # pylint: disable=arguments-differ
        """Runs before each test method.

        Sets up a mock database collection table for 'topics'.
        """
        self.mock_table = MagicMock()
        mock_db_conn_class.return_value.get_table.return_value = self.mock_table

        self.controller = TopicController()
        mock_db_conn_class.assert_called_once_with("topics")

        # Test fixtures for BSON ObjectIds
        self.dummy_category_id_str = "507f1f77bcf86cd799439011"
        self.dummy_category_oid = ObjectId(self.dummy_category_id_str)
        self.dummy_topic_id = ObjectId("507f1f77bcf86cd799439022")

    # -------------------------------------------------------------------------
    # Tests for create_topic
    # -------------------------------------------------------------------------

    def test_create_topic_returns_false_when_already_exists(self):
        """Validate no duplicate topics"""
        # Arrange: simulate topic already exists in the given category
        self.mock_table.count_documents.return_value = 1

        # Act
        result = self.controller.create_topic(
            name="python",
            topic_type="coding",
            category_id=self.dummy_category_id_str,
            metadata="test metadata",
        )

        # Assert
        self.mock_table.count_documents.assert_called_once_with(
            {"name": "python", "category_id": self.dummy_category_oid}
        )
        self.mock_table.insert_one.assert_not_called()
        self.assertFalse(result)

    def test_create_topic_success_when_new(self):
        # Arrange: topic does not exist yet
        self.mock_table.count_documents.return_value = 0
        expected_doc = {
            "_id": self.dummy_topic_id,
            "name": "python",
            "type": "coding",
            "category_id": self.dummy_category_oid,
            "metadata": "test metadata",
        }
        self.mock_table.find_one.return_value = expected_doc

        # Act
        result = self.controller.create_topic(
            name="python",
            topic_type="coding",
            category_id=self.dummy_category_id_str,
            metadata="test metadata",
        )

        # Assert
        self.mock_table.count_documents.assert_called_once_with(
            {"name": "python", "category_id": self.dummy_category_oid}
        )
        self.mock_table.insert_one.assert_called_once_with(
            {
                "name": "python",
                "type": "coding",
                "category_id": self.dummy_category_oid,
                "metadata": "test metadata",
            }
        )
        self.mock_table.find_one.assert_called_once_with(
            {"name": "python", "category_id": self.dummy_category_oid}
        )
        self.assertEqual(result, expected_doc)

    # -------------------------------------------------------------------------
    # Tests for retrieve_topics
    # -------------------------------------------------------------------------

    def test_retrieve_topics_returns_matching_list(self):
        """Validate retrieve"""
        # Arrange
        mock_topics = [
            {
                "_id": self.dummy_topic_id,
                "name": "general",
                "type": "general",
                "category_id": self.dummy_category_oid,
                "metadata": "",
            },
            {
                "_id": ObjectId("507f1f77bcf86cd799439033"),
                "name": "announcements",
                "type": "news",
                "category_id": self.dummy_category_oid,
                "metadata": "",
            },
        ]
        self.mock_table.find.return_value = mock_topics

        # Act
        result = self.controller.retrieve_topics(self.dummy_category_id_str)

        # Assert
        self.mock_table.find.assert_called_once_with(
            {"category_id": self.dummy_category_oid}
        )
        self.assertEqual(result, mock_topics)

    # -------------------------------------------------------------------------
    # Tests for general_landing
    # -------------------------------------------------------------------------

    def test_general_landing_returns_existing_general_topic(self):
        """Validate initial page load works"""
        # Arrange: general topic already exists for this category
        self.mock_table.count_documents.return_value = 1
        expected_topic = {
            "_id": self.dummy_topic_id,
            "name": "general",
            "type": "general",
            "category_id": self.dummy_category_oid,
            "metadata": "",
        }
        self.mock_table.find_one.return_value = expected_topic

        # Act
        result = self.controller.general_landing(self.dummy_category_id_str)

        # Assert
        self.mock_table.count_documents.assert_called_once_with(
            {"name": "general", "category_id": self.dummy_category_oid}
        )
        self.mock_table.find_one.assert_called_once_with(
            {"name": "general", "category_id": self.dummy_category_oid}
        )
        self.mock_table.insert_one.assert_not_called()
        self.assertEqual(result, expected_topic)

    @patch.object(TopicController, "create_topic")
    def test_general_landing_creates_general_topic_when_not_found(
        self, mock_create_topic
    ):
        """Validate we create a new topic if first user"""
        # Arrange: general topic does not exist
        self.mock_table.count_documents.return_value = 0
        expected_topic = {
            "_id": self.dummy_topic_id,
            "name": "general",
            "type": "general",
            "category_id": self.dummy_category_oid,
            "metadata": "",
        }
        mock_create_topic.return_value = expected_topic

        # Act
        result = self.controller.general_landing(self.dummy_category_id_str)

        # Assert
        self.mock_table.count_documents.assert_called_once_with(
            {"name": "general", "category_id": self.dummy_category_oid}
        )
        # Note: general_landing converts category_id to ObjectId prior to calling create_topic
        mock_create_topic.assert_called_once_with(
            name="general",
            topic_type="general",
            category_id=self.dummy_category_oid,
        )
        self.assertEqual(result, expected_topic)
