from database.mongodb_connection import mongodb_connection
import pprint

class category_controller():
    def __init__(self): 
        self.dbconnection = mongodb_connection("category").get_table()

    def create_category(self, name, joinable):
        if self.dbconnection.count_documents({"name" : name, "joinable" : joinable}) > 0:
            return False
        self.dbconnection.insert_one({"name" : name, "joinable" : joinable})

    def list_categories(self):
        ret = []
        categories = self.dbconnection.find({"joinable" : True})
        for item in categories:
            ret.append(item)
        return ret
