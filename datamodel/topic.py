"""Data Model for the Topic Type"""
from typing import TypedDict
from flask_restx import fields

class Topic(TypedDict):
    """Basic Data Model for the Topic Type"""
    category_id: str
    metadata:str
    topic: str
    type: str

class ApiTopic():
    """API Model for the Topic Type"""
    def __init__(self, api):
        self.model = api.model('Topic', {
            'category_id': fields.String(description='category_id'),
            'name': fields.String(description='name'),
            'type': fields.String(description='type'),
            'metadata': fields.String(description='metadata'),
            '_id' : fields.String(description='topic_id')
            # Metadata is just mocked in for now
        })
        self.list = api.model('TopicList', { 'topics' : fields.List(fields.Nested(self.model))})

    def get_model(self):
        """Return the API Moel""" 
        return self.model

    def get_list(self):
        """Return the List Structure for the model"""
        return self.list
