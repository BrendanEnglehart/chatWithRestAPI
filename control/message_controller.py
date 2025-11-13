import datetime

from database.mongodb_connection import mongodb_connection


class message_controller():
    def __init__(self): 
        self.dbconnection = mongodb_connection("messages").get_table()

    def create_message(self, username, picture, topic, text):
        print(username)
        self.dbconnection.insert_one({"username": username, "time": datetime.datetime.now(), "deleted" :False, "picture":picture, "topic": topic, "text": text})
        return True
    
    def get_messages(self, topic):
        messages = self.dbconnection.find({"topic": topic, "deleted": False}, sort={"time" : 1}, limit=100)
        ret = []
        for message in messages:
            ret.append(message)

        return {"messages": ret}

    def get_message_stream(self, topic, time):
        print(time)
        print(topic)
        messages = self.dbconnection.find({"topic": topic,
                                            "deleted": False, 
                                            "time": {"$gt": datetime.datetime.fromisoformat(time)}
                                           }, 
                                           sort={"time" : 1}, 
                                           limit=100)
        ret = []
        
        for message in messages:
            ret.append(message)

        print(ret)
        return {"messages": ret}