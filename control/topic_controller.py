"""
Controller for the Topic Objects
Topics contain chat messages and a type
In the future they will contain metadata that pertains to
the specific topic
"""

from bson.objectid import ObjectId
from database.mongodb_connection import MongoDBConnection
from datamodel.topic import Topic
from control.category_controller import CategoryController


class TopicController:
    """Topic Controller"""

    def __init__(self):
        self.dbconnection = MongoDBConnection("topics").get_table()

    def create_topic(self, name, topic_type, category_id, metadata="") -> Topic:
        """Create a topic"""
        if (
            self.dbconnection.count_documents(
                {"name": name, "category_id": ObjectId(category_id)}
            )
            > 0
        ):
            return False
        self.dbconnection.insert_one(
            {
                "name": name,
                "type": topic_type,
                "category_id": ObjectId(category_id),
                "metadata": metadata,
            }
        )
        return self.dbconnection.find_one(
            {"name": name, "category_id": ObjectId(category_id)}
        )

    def retrieve_topics(self, category_id) -> list:
        """retrieve all topics matching a category id"""
        topics = self.dbconnection.find({"category_id": ObjectId(category_id)})
        ret = []
        for topic in topics:
            ret.append(topic)
        return ret

    def general_landing(self, category_id) -> Topic:
        """retrieve the General topic or create it"""
        if (
            self.dbconnection.count_documents(
                {"name": "general", "category_id": ObjectId(category_id)}
            )
            > 0
        ):
            return self.dbconnection.find_one(
                {"name": "general", "category_id": ObjectId(category_id)}
            )
        return self.create_topic(
            name="general", topic_type="general", category_id=ObjectId(category_id)
        )

    def direct_message_topic(self, user_id_list, category_id=None, metadata=""):
        """return a direct message topic for a user or groups of users"""
        if category_id is None:
            cc = CategoryController()
            category_id = cc.find_or_create_category("direct_messages", False).get_id()

        if (
            self.dbconnection.count_documents(
                {
                    "user_id_list": user_id_list,
                    "category_id": ObjectId(category_id),
                }
            )
            == 0
        ):
            self.dbconnection.insert_one(
                {
                    "name": "direct_message",
                    "category_id": category_id,
                    "user_id_list": user_id_list,
                    "metadata": metadata,
                }
            )
