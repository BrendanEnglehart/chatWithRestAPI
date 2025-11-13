import certifi
from pymongo.mongo_client import MongoClient
from os import environ
from dotenv import find_dotenv, load_dotenv

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)
uri =environ.get('URI')
print(uri)
# Create a new client and connect to the server
client = MongoClient(uri, tlsCAFile=certifi.where()
                    ) # garbage that won't make it into production but exists here for testing
# Establish the database we are accessing
database = client["Chat"]
## I'm creating a basic shell for this
# TODO: come back and fix this more later
class mongodb_connection(): 
    def __init__(self, table):
        # All of the connections use the client no matter where we instantiate it. 
        # print(hex(id(client)))
        self.table = database[table]
    
    def get_table(self):
        return self.table
    



