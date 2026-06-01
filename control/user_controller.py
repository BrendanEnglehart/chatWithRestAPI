"""
User Controller
Needs a rewrite now that I've switched to Auth0
"""
from database.mongodb_connection import MongoDBConnection


class UserController():
    """Controls all user operations"""
    def __init__(self):
        self.dbconnection = MongoDBConnection("users").get_table()

    def create_or_retrieve_user(self, user):
        """Create A User
            User Creation really happens in Auth0, 
            this just initializes personal info on the server
        """
        cursor = self.dbconnection.count_documents({"auth_id" : user["auth_id"]})
        if cursor == 0:
            self.dbconnection.insert_one(user)
        return self.dbconnection.find_one({"auth_id" : user["auth_id"]})
    
    def update_username(self, user_id, username):
        """Update Username"""
        print (username, "here" )
        query_filter = {'auth_id': user_id}
        print (username, "here2" )
        update_operation = { '$set' :
           {'username' : username}
        }
        print (username, "here3" )
        result = self.dbconnection.update_one(query_filter, update_operation)
        print (result )
        return self.dbconnection.find_one({"auth_id" : user_id})
        


    def get_user(self, username):
        """Retrieve User information"""
        user= self.dbconnection.find_one({"username" : username})
        return {user["username"], user["email"]}

    def get_users(self):
        """Retrieve a list of Users"""
        cursor = self.dbconnection.find()
        ret = []
        # we could do this in a 1 liner, but the reason not to is because this isn't my final form!
        for user in cursor:
            ret.append(user)
        
        return ret


    def login(self, username, picture):
        """Login to the app"""
        cursor = self.dbconnection.count_documents({"username" : username, "picture":picture})
        if cursor==0:
            cursor = self.dbconnection.count_documents({"email" : username, "picture":picture})
        return cursor==1        