from typing import TypedDict
from flask_restx import fields

class User(TypedDict):
    category_id: str
    username: str
    email: str
    picture: str


class ApiUser():
    def __init__(self, api):
        self.model = api.model('RecieveUser', {
            'username': fields.String(description='Username'),
            'email': fields.String(description='Email'),
            'picture': fields.String(description='Picture'),
            'category_id': fields.String(description='category id')
        })

    def Model(self): 
        return self.model
    

class ReturnUser():
    def __init__(self, api):
        self.model = api.model('User', {
            'username': fields.String(description='Username'),
            'email': fields.String(description='Email'),
            'picture': fields.String(description='Picture'),
        })

    def Model(self): 
        return self.model