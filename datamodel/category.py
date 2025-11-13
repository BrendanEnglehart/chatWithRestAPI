from typing import TypedDict
from flask_restx import fields

class Category(TypedDict):
    name: str
    joinable: bool



class ApiCategory():
    def __init__(self, api):
        self.scaffold =  {
            '_id': fields.String(description='category_id'),
            'name': fields.String(description='name'),
            'joinable': fields.Boolean(description='public category (i.e. general) vs user chats'),
        }
        self.model=api.model('Category', self.scaffold)
        self.list = api.model('CategoryList', { 'categories' : fields.List(fields.Nested(self.model))})
    
    def Model(self): 
        return self.model
    
    def List(self):
        return self.list
    