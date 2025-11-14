from database.mongodb_connection import MongoDBConnection


class CategoryController():
    """Controller for the Category Objects
    Categories are lists of Topics
    """
    def __init__(self):
        self.dbconnection = MongoDBConnection("category").get_table()

    def create_category(self, name, joinable):
        """Handles Category Creation Logic"""
        if self.dbconnection.count_documents({"name" : name, "joinable" : joinable}) > 0:
            return False
        self.dbconnection.insert_one({"name" : name, "joinable" : joinable})
        return self.dbconnection.find_one({"name" : name, "joinable" : joinable})

    def list_categories(self):
        """Lists all categories that are joinable"""
        ret = []
        categories = self.dbconnection.find({"joinable" : True})
        for item in categories:
            ret.append(item)
        return ret

    def find_category(self, name, joinable):
        """Finds a particular category and returns it if able"""
        return self.dbconnection.find_one({"name" : name, "joinable" : joinable})
    
    def general_landing(self):
        "Find the General Category or create it if it doesn't exist"
        name, joinable = "general", True
        if self.dbconnection.count_documents({"name" : name, "joinable" : joinable}) > 0:
            return self.dbconnection.find_one({"name" : name, "joinable" : joinable})
        return self.create_category(name, joinable)