from database.mongodb_connection import mongodb_connection
from datamodel.topic import Topic


class topic_controller():
    def __init__(self): 
        self.dbconnection = mongodb_connection("topics").get_table()

    def create_topic(self, name, type, category_id):
        self.dbconnection.insert_one({"name" : name, "type" : type, "category_id" : category_id})
        return True

    def retrieve_topics(self, category_id):
        topics = self.dbconnection.find({"category_id" : category_id})
        ret = []
        for topic in topics:
            ret.append(topic)
        return ret
