"""
Controller for the Topic Objects
Topics contain chat messages and a type
In the future they will contain metadata that pertains to 
the specific topic
"""

from database.mongodb_connection import MongoDBConnection

class TopicController():
    """Topic Controller"""
    def __init__(self): 
        self.dbconnection = MongoDBConnection("topics").get_table()

    def create_topic(self, name, topic_type, category_id):
        """Create a topic"""
        self.dbconnection.insert_one({"name" : name, "type" : topic_type, "category_id" : category_id})
        return True

    def retrieve_topics(self, category_id):
        """retrieve all topics matching a category id"""
        topics = self.dbconnection.find({"category_id" : category_id})
        ret = []
        for topic in topics:
            ret.append(topic)
        return ret
