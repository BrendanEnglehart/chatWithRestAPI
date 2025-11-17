"""
Controller for the Topic Objects
Topics contain chat messages and a type
In the future they will contain metadata that pertains to
the specific topic
"""

from database.mongodb_connection import MongoDBConnection


class TopicController:
    """Topic Controller"""

    def __init__(self):
        self.dbconnection = MongoDBConnection("topics").get_table()

    def create_topic(self, name, topic_type, category_id, metadata=""):
        """Create a topic"""
        if (
            self.dbconnection.count_documents(
                {"name": name, "category_id": category_id}
            )
            > 0
        ):
            return False
        self.dbconnection.insert_one(
            {
                "name": name,
                "type": topic_type,
                "category_id": category_id,
                "metadata": metadata,
            }
        )
        return self.dbconnection.find_one({"name": name, "category_id": category_id})

    def retrieve_topics(self, category_id):
        """retrieve all topics matching a category id"""
        topics = self.dbconnection.find({"category_id": category_id})
        ret = []
        for topic in topics:
            ret.append(topic)
        return ret

    def general_landing(self, category_id):
        """retrieve the General topic or create it"""
        if (
            self.dbconnection.count_documents(
                {"name": "general", "category_id": category_id}
            )
            > 0
        ):
            return self.dbconnection.find_one(
                {"name": "general", "category_id": category_id}
            )
        return self.create_topic(
            name="general", topic_type="general", category_id=category_id
        )
