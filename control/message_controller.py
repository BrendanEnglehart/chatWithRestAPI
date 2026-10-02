"""Logic for controlling message flow"""

import datetime
from bson.objectid import ObjectId
from database.mongodb_connection import MongoDBConnection


class MessageController:
    """Controller for sending and recieving messages"""

    def __init__(self):
        self.dbconnection = MongoDBConnection("messages").get_table()

    def create_message(self, user_id, topic, text):
        """Create a message"""
        time = datetime.datetime.now()
        self.dbconnection.insert_one(
            {
                "user_id": ObjectId(user_id),
                "time": time,
                "deleted": False,
                "topic": ObjectId(topic),
                "text": text,
            }
        )
        ret = self.dbconnection.find_one(
            {
                "user_id": ObjectId(user_id),
                "time": time,
                "deleted": False,
                "topic": ObjectId(topic),
                "text": text,
            }
        )
        return ret

    def edit_message(self, user_id, _id, text):
        """Edit a message"""
        self.dbconnection.update_one(
            {"user_id": ObjectId(user_id), "_id": ObjectId(_id)},
            {
                "$set": {
                    "text": text,
                }
            },
        )
        ret = self.dbconnection.find_one(
            {
                "user_id": ObjectId(user_id),
                "_id": ObjectId(_id),
            }
        )
        return ret

    def delete_message(self, _id, user_id):
        """Flags a message for deletion"""
        self.dbconnection.update_one(
            {"user_id": ObjectId(user_id), "_id": ObjectId(_id)},
            {"$set": {"deleted": True}},
        )

    def get_messages(self, topic):
        """Return messages"""
        messages = self.dbconnection.find(
            {"topic": ObjectId(topic), "deleted": False}, sort={"time": 1}, limit=100
        )
        ret = []
        for message in messages:
            ret.append(message)

        return {"messages": ret}

    # Get feed messages vs get message feed.
    # feed_messages sounds wrong but is more of what it's doing
    # message_feed wouldn't really confuse anyone.
    def get_feed_messages(self, topic, time, size=100):
        """Return messages from before a certain time"""
        messages = self.dbconnection.find(
            {"topic": ObjectId(topic), "deleted": False, "time": {"$lt": time}},
            sort={"time": -1},
            limit=size,
        )
        ret = []
        for message in messages:
            ret.append(message)

        return {"messages": ret[::-1]}

    def get_next_page_messages(self, topic, size=100, page=0):
        """Return messages paginated
        # this is less performance friendly
        Use get_feed unless you really need the paginated form
        """
        messages = self.dbconnection.find(
            {"topic": ObjectId(topic), "deleted": False},
            sort={"time": -1},
            limit=size,
            skip=size * page,
        )
        ret = []
        for message in messages:
            ret.append(message)

        return {"messages": ret[::-1]}

    def get_message_stream(self, topic, time):
        """Return a set of messages after a time,
        In the future calling this request
        will start up a streaming connections instead"""
        messages = self.dbconnection.find(
            {
                "topic": ObjectId(topic),
                "deleted": False,
                "time": {"$gt": datetime.datetime.fromisoformat(time)},
            },
            sort={"time": -1},
            limit=100,
        )
        ret = []

        for message in messages:
            ret.append(message)

        return {"messages": ret[::-1]}
