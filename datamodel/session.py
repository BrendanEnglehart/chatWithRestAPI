from typing import TypedDict
from datetime import datetime
from flask_restx import fields

class Session(TypedDict):
    session_key: str
    username: str
    expires: datetime

class ApiSession():
    def __init__(self, api):
        self.model = api.model('Session', {
            '_id': fields.String(description='session_key'),
            'username': fields.String(description='username'),
            'expires': fields.DateTime(description='expires'),
        })

    def Model(self): 
        return self.model
    
