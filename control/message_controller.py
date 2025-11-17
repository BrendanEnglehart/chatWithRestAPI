"""Logic for controlling message flow"""

import datetime

from database.mongodb_connection import MongoDBConnection


class message_controller:
    """Controller for sending and recieving messages"""

    def __init__(self):
        self.dbconnection = MongoDBConnection("messages").get_table()

    def create_message(self, username, picture, topic, text):
        """Create a message"""
        self.dbconnection.insert_one(
            {
                "username": username,
                "time": datetime.datetime.now(),
                "deleted": False,
                "picture": picture,
                "topic": topic,
                "text": text,
            }
        )
        return True

    def get_messages(self, topic):
        """Return messages"""
        messages = self.dbconnection.find(
            {"topic": topic, "deleted": False}, sort={"time": 1}, limit=100
        )
        ret = []
        for message in messages:
            ret.append(message)

        return {"messages": ret}

    def get_message_stream(self, topic, time):
        """Return a set of messages after a time, 
        In the future calling this request 
        will start up a streaming connections instead"""
        messages = self.dbconnection.find(
            {
                "topic": topic,
                "deleted": False,
                "time": {"$gt": datetime.datetime.fromisoformat(time)},
            },
            sort={"time": 1},
            limit=100,
        )
        ret = []

        for message in messages:
            ret.append(message)

        print(ret)
        return {"messages": ret}
