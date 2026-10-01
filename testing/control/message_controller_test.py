"""Message controller Unit test framework"""

import datetime
import unittest
from unittest.mock import MagicMock, patch
from bson.objectid import ObjectId

from control.message_controller import MessageController


class TestMessageController(unittest.TestCase):
    """Test Suite for messages"""

    @patch("control.message_controller.MongoDBConnection")
    def setUp(self, mock_db_conn_class):  # pylint: disable=arguments-differ
        """Runs before each test method.

        Sets up a mock database collection table for 'messages'.
        """
        self.mock_table = MagicMock()
        mock_db_conn_class.return_value.get_table.return_value = self.mock_table

        self.controller = MessageController()
        mock_db_conn_class.assert_called_once_with("messages")

        # Useful reusable BSON ObjectIds for test fixtures
        self.dummy_user_id_str = "507f1f77bcf86cd799439011"
        self.dummy_topic_id_str = "507f1f77bcf86cd799439022"
        self.dummy_msg_id_str = "507f1f77bcf86cd799439033"

    # -------------------------------------------------------------------------
    # Tests for create_message
    # -------------------------------------------------------------------------

    @patch("control.message_controller.datetime")
    def test_create_message_success(self, mock_datetime):
        """Validate message creation"""
        # Arrange
        fixed_now = datetime.datetime(2026, 1, 1, 12, 0, 0)
        mock_datetime.datetime.now.return_value = fixed_now

        expected_filter = {
            "user_id": ObjectId(self.dummy_user_id_str),
            "time": fixed_now,
            "deleted": False,
            "topic": ObjectId(self.dummy_topic_id_str),
            "text": "Hello World",
        }
        expected_msg = {**expected_filter, "_id": ObjectId(self.dummy_msg_id_str)}
        self.mock_table.find_one.return_value = expected_msg

        # Act
        result = self.controller.create_message(
            user_id=self.dummy_user_id_str,
            topic=self.dummy_topic_id_str,
            text="Hello World",
        )

        # Assert
        self.mock_table.insert_one.assert_called_once_with(expected_filter)
        self.mock_table.find_one.assert_called_once_with(expected_filter)
        self.assertEqual(result, expected_msg)

    # -------------------------------------------------------------------------
    # Tests for edit_message
    # -------------------------------------------------------------------------

    def test_edit_message_success(self):
        """Test editing messages"""
        # Arrange
        expected_query = {
            "user_id": ObjectId(self.dummy_user_id_str),
            "_id": ObjectId(self.dummy_msg_id_str),
        }
        updated_msg = {
            "_id": ObjectId(self.dummy_msg_id_str),
            "user_id": ObjectId(self.dummy_user_id_str),
            "text": "Updated text",
        }
        self.mock_table.find_one.return_value = updated_msg

        # Act
        result = self.controller.edit_message(
            user_id=self.dummy_user_id_str,
            _id=self.dummy_msg_id_str,
            text="Updated text",
        )

        # Assert
        self.mock_table.update_one.assert_called_once_with(
            expected_query, {"$set": {"text": "Updated text"}}
        )
        self.mock_table.find_one.assert_called_once_with(expected_query)
        self.assertEqual(result, updated_msg)

    # -------------------------------------------------------------------------
    # Tests for delete_message
    # -------------------------------------------------------------------------

    def test_delete_message_flags_deleted_true(self):
        """Validate we flag the deleted objects as deleted"""
        # Act
        self.controller.delete_message(
            _id=self.dummy_msg_id_str, user_id=self.dummy_user_id_str
        )

        # Assert
        expected_query = {
            "user_id": ObjectId(self.dummy_user_id_str),
            "_id": ObjectId(self.dummy_msg_id_str),
        }
        self.mock_table.update_one.assert_called_once_with(
            expected_query, {"$set": {"deleted": True}}
        )

    # -------------------------------------------------------------------------
    # Tests for get_messages
    # -------------------------------------------------------------------------

    def test_get_messages_returns_formatted_dict(self):
        """Validate we can still parse this on the other side"""
        # Arrange
        mock_messages = [
            {"_id": ObjectId(self.dummy_msg_id_str), "text": "First"},
            {"_id": ObjectId(), "text": "Second"},
        ]
        self.mock_table.find.return_value = mock_messages

        # Act
        result = self.controller.get_messages(topic=self.dummy_topic_id_str)

        # Assert
        self.mock_table.find.assert_called_once_with(
            {"topic": ObjectId(self.dummy_topic_id_str), "deleted": False},
            sort={"time": 1},
            limit=100,
        )
        self.assertEqual(result, {"messages": mock_messages})

    # -------------------------------------------------------------------------
    # Tests for get_message_stream
    # -------------------------------------------------------------------------

    def test_get_message_stream_parses_iso_time(self):
        """This test is probably superfluous"""
        # Arrange
        iso_time_str = "2026-01-01T12:00:00"
        parsed_datetime = datetime.datetime.fromisoformat(iso_time_str)

        mock_messages = [
            {"_id": ObjectId(self.dummy_msg_id_str), "text": "New message"}
        ]
        self.mock_table.find.return_value = mock_messages

        # Act
        result = self.controller.get_message_stream(
            topic=self.dummy_topic_id_str, time=iso_time_str
        )

        # Assert
        self.mock_table.find.assert_called_once_with(
            {
                "topic": ObjectId(self.dummy_topic_id_str),
                "deleted": False,
                "time": {"$gt": parsed_datetime},
            },
            sort={"time": 1},
            limit=100,
        )
        self.assertEqual(result, {"messages": mock_messages})

    # -------------------------------------------------------------------------
    # Tests for get_feed_messages
    # -------------------------------------------------------------------------

    def test_get_feed_messages_default_parameters(self):
        """Validates we get all messages"""
        # Arrange
        mock_messages = [
            {"_id": ObjectId(), "text": "Msg 1"},
            {"_id": ObjectId(), "text": "Msg 2"},
        ]
        self.mock_table.find.return_value = mock_messages
        now = datetime.datetime.now()
        # Act
        result = self.controller.get_feed_messages(
            topic=self.dummy_topic_id_str, time=now
        )

        # Assert
        self.mock_table.find.assert_called_once_with(
            {
                "topic": ObjectId(self.dummy_topic_id_str),
                "deleted": False,
                "time": {"$lt": now},
            },
            sort={"time": 1},
            limit=100,
        )
        self.assertEqual(result, {"messages": mock_messages})

    def test_get_feed_messages_custom_time_and_size(self):
        """validates we only pull after some date/time"""
        # Arrange
        custom_time = datetime.datetime(2026, 10, 1, 12, 0, 0)
        custom_size = 25
        mock_messages = [{"_id": ObjectId(), "text": "Older Msg"}]
        self.mock_table.find.return_value = mock_messages

        # Act
        result = self.controller.get_feed_messages(
            topic=self.dummy_topic_id_str, time=custom_time, size=custom_size
        )

        # Assert
        self.mock_table.find.assert_called_once_with(
            {
                "topic": ObjectId(self.dummy_topic_id_str),
                "deleted": False,
                "time": {"$lt": custom_time},
            },
            sort={"time": 1},
            limit=25,
        )
        self.assertEqual(result, {"messages": mock_messages})

        # -------------------------------------------------------------------------

    # Tests for get_next_page_messages
    # -------------------------------------------------------------------------

    def test_get_next_page_messages_first_page(self):
        """Validate function works"""
        # Arrange: Page 0 (default) with custom size
        mock_messages = [{"_id": ObjectId(), "text": "Page 0 Msg"}]
        self.mock_table.find.return_value = mock_messages

        # Act
        result = self.controller.get_next_page_messages(
            topic=self.dummy_topic_id_str, size=20, page=0
        )

        # Assert
        self.mock_table.find.assert_called_once_with(
            {"topic": ObjectId(self.dummy_topic_id_str), "deleted": False},
            sort={"time": 1},
            limit=20,
            skip=0,  # 20 * 0
        )
        self.assertEqual(result, {"messages": mock_messages})

    def test_get_next_page_messages_subsequent_page(self):
        """We enforce the return value here, so we aren't actually testing pagination
        What we want to validate is that 
        we do infact call the function 
        and we haven't massively broken the function call
        """
        # Arrange: Page 2 with size 50 -> skip = 100
        mock_messages = [{"_id": ObjectId(), "text": "Page 2 Msg"}]
        self.mock_table.find.return_value = mock_messages

        # Act
        result = self.controller.get_next_page_messages(
            topic=ObjectId(self.dummy_topic_id_str), size=50, page=2
        )

        # Assert
        self.mock_table.find.assert_called_once_with(
            {"topic": ObjectId(self.dummy_topic_id_str), "deleted": False},
            sort={"time": 1},
            limit=50,
            skip=100,  # 50 * 2
        )
        self.assertEqual(result, {"messages": mock_messages})
