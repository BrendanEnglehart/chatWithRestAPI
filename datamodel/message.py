from typing import TypedDict
from datetime import datetime
from flask_restx import fields

class Message(TypedDict):
    username: str
    topic: str
    text: str
    time: datetime
    deleted: bool
    session: str
    

class ApiMessage():
    def __init__(self, api):
        self.scaffold = {
            'username': fields.String(description='username'),
            'time': fields.DateTime(description='time'),
            'topic': fields.String(description='topic'),
            'text': fields.String(description="text"),
            'picture': fields.String(description="picture")
        }
        self.model = api.model('Message', self.scaffold)
        self.list = api.model('MessageList', { 'messages' : fields.List(fields.Nested(self.model))})

    def Model(self): 
        return self.model
    
    def List(self):
        return  self.list

