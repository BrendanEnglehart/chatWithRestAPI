from datamodel.message import ApiMessage
from flask import Blueprint
from flask_restx import Api, Resource
from control.message_controller import message_controller

from datamodel.message import ApiMessage


bp = Blueprint('messages', __name__)
api = Api(bp, version='1.0', title='API',
    description='An API',
)
ns = api.namespace('', description='Messaging Logic')



messageModel = ApiMessage(api).Model()
messagesModel = ApiMessage(api).List()
messages = message_controller()

@ns.route('/<string:topic>')
@ns.response(404, 'Topic not found')
@ns.param('topic', 'The topic to retrieve')
class MessageAPI(Resource):
    '''Gets messages - We'll want to add a limit to how many messages we pull TODO!!!!'''
    @ns.doc('get_messages')
    @ns.marshal_with(messagesModel)
    def get(self, topic):
        '''Fetch a given resource'''
        return messages.get_messages(topic=topic)
    
    @ns.doc('send_message')
    @ns.marshal_with(messageModel)
    @ns.expect(messageModel)
    def post(self, topic):
        '''Fetch a given resource'''
        return messages.create_message(username=api.payload["username"], picture=api.payload["picture"], topic=topic, text=api.payload["text"])
    
@ns.route('/stream/topic=<string:topic>&time=<string:time>')
@ns.response(404, 'Topic not found')
@ns.param('topic', 'The topic to retrieve')
@ns.param('time', 'The time after which to receive messages')
class MessageStreamAPI(Resource):
    '''Gets messages - We'll want to add a limit to how many messages we pull TODO!!!!'''
    @ns.doc('get_message_stream')
    @ns.marshal_with(messagesModel)
    def get(self, topic, time):
        '''Fetch a given resource'''
        print(time)
        if time == 0:
            return []
        return messages.get_message_stream(topic=topic, time=time)
    
   


