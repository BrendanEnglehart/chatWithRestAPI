import datetime

from database.mongodb_connection import mongodb_connection

# TODO: Session's need to only be valid for a day
SESSION_LENGTH = datetime.timedelta(days=365)


class session_controller():
    def __init__(self): 
        self.dbconnection = mongodb_connection("session").get_table()

    def create_session(self, username):
        self.dbconnection.insert_one({"username": username, "expires": datetime.datetime.now() + SESSION_LENGTH})
        session= self.dbconnection.find_one({"username": username, "expires" : {"$gt" : datetime.datetime.now()}})
        return session
    
    def valid_session(self, session_id):
        return self.dbconnection.count({"_id":session_id, "expires":{"$gt": datetime.datetime.now}}) > 0
    
