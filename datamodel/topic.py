from typing import TypedDict
from flask_restx import fields

class Topic(TypedDict):
    category_id: str
    topic: str
    type: str
    
class ApiTopic():
    def __init__(self, api):
        self.model = api.model('Topic', {
            'category_id': fields.String(description='category_id'),
            'name': fields.String(description='name'),
            'type': fields.String(description='type'),
        })
        self.list = api.model('TopicList', { 'topics' : fields.List(fields.Nested(self.model))})

    def Model(self): 
        return self.model
    
    def List(self):
        return self.list