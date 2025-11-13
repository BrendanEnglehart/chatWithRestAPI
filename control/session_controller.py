"""
Deprecated with the new AUTH logic.
Some Developer features are still accessing the session logic
This will be removed on a future pass
"""
import datetime

from database.mongodb_connection import MongoDBConnection

SESSION_LENGTH = datetime.timedelta(days=1)


class SessionController():
    """Controller for the session Objects"""
    def __init__(self): 
        self.dbconnection = MongoDBConnection("session").get_table()

    def create_session(self, username):
        """Create a session"""
        self.dbconnection.insert_one({"username": username, "expires": datetime.datetime.now() + SESSION_LENGTH})
        session= self.dbconnection.find_one({"username": username, "expires" : {"$gt" : datetime.datetime.now()}})
        return session
    
    def valid_session(self, session_id):
        """Check if a session is valid before accepting messages"""
        return self.dbconnection.count({"_id":session_id, "expires":{"$gt": datetime.datetime.now}}) > 0
    
