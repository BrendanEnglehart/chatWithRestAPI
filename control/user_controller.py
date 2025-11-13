from database.mongodb_connection import mongodb_connection
from datamodel.user import User


class user_controller():
    def __init__(self): 
        self.dbconnection = mongodb_connection("users").get_table()
    
    def create_user(self, username, email, picture):
        cursor = self.dbconnection.count_documents({"username" : username})
        if cursor == 0:
                #personal_category = self.dbconnection.find({"category":username, "joinable":False})[0]._id
                new_user = User(username=username, email=email, picture=picture, category_id=0)
                self.dbconnection.insert_one(new_user)

    def get_user(self, username):
        user= self.dbconnection.find_one({"username" : username})
        return {user["username"], user["email"]}
        



    def get_users(self):
        cursor = self.dbconnection.find({"username": {"$exists" : "true"}})
        ret = []
        # we could do this in a 1 liner, but the reason not to is because this isn't my final form!
        for user in cursor:
            ret.append(user['username'])
        
        return ret


    def login(self, username, picture):
        cursor = self.dbconnection.count_documents({"username" : username, "picture":picture})
        if cursor==0:
            cursor = self.dbconnection.count_documents({"email" : username, "picture":picture})
        return cursor==1        