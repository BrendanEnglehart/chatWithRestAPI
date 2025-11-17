"""Data Structures for the Category Objects"""

from typing import TypedDict
from flask_restx import fields


class Category(TypedDict):
    """Data Structure for the Category Objects"""

    name: str
    joinable: bool


class ApiCategory:
    """API Data Structures for the Category Object"""

    def __init__(self, api):
        self.scaffold = {
            "_id": fields.String(description="category_id"),
            "name": fields.String(description="name"),
            "joinable": fields.Boolean(
                description="public category (i.e. general) vs user chats"
            ),
        }
        self.model = api.model("Category", self.scaffold)
        self.list = api.model(
            "CategoryList", {"categories": fields.List(fields.Nested(self.model))}
        )

    def get_model(self):
        """Get the model object"""
        return self.model

    def get_list(self):
        """Return the List Structure for the model"""
        return self.list
