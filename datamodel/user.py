"""User Class Data Models"""
from typing import TypedDict
from flask_restx import fields

class User(TypedDict):
    """User Class object"""
    auth_id: str
    category_id: str
    username: str
    email: str
    picture: str


class ApiUser():
    """The API user model we recieve"""
    def __init__(self, api):
        self.model = api.model('RecieveUser', {
            'auth_id' : fields.String(description='auth_id'),
            'username': fields.String(description='Username'),
            'email': fields.String(description='Email'),
            'picture': fields.String(description='Picture'),
            'category_id': fields.String(description='category id')
        })

    def get_model(self):
        """Return the self model reference"""
        return self.model
    

class ReturnUser():
    """The API user model we send back to the server"""
    def __init__(self, api):
        self.model = api.model('User', {
            'username': fields.String(description='Username'),
            'email': fields.String(description='Email'),
            'picture': fields.String(description='Picture'),
            '_id': fields.String(description='User ID')
        })

    def get_model(self):
        """Return the API Moel"""
        return self.model