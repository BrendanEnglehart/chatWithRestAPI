"""Loads the mongo DB connection client"""

from os import environ
import certifi
from pymongo.mongo_client import MongoClient
from dotenv import find_dotenv, load_dotenv

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)
uri = environ.get("URI")
# Create a new client and connect to the server
client = MongoClient(
    uri, tlsCAFile=certifi.where()
)
# Establish the database we are accessing
database = client["Chat"]


class MongoDBConnection:
    """Class MongoDBConnection: Allows for easy, repeatable access to the MongoDB connections"""

    def __init__(self, table):
        """
        # Table is the name of the table you wish to acess
        # All of the connections use the same client no matter where we instantiate it.
        # print(hex(id(client)))
        """
        self.table = database[table]

    def get_table(self):
        """Returns the table for easy access"""
        return self.table

    def quick_select(self):
        """Returns all entries on the table"""
        return self.table.find()
