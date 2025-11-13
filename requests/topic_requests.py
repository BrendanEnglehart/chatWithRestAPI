from flask import Blueprint
from flask_restx import Api, Resource

from control.user_controller import user_controller
from flask import Blueprint
from flask_restx import Api, Resource

from datamodel.user import ApiUser, ReturnUser
from datamodel.topic import ApiTopic
from control.topic_controller import topic_controller

TopicBlueprint = Blueprint('topic', __name__)
api = Api(TopicBlueprint, version='1.0', title='API',
    description='An API',
)
ns = api.namespace('', description='topic Logic')

topicModel = ApiTopic(api).Model()
topicListModel = ApiTopic(api).List()
topic = topic_controller()
@ns.route('/<string:category_id>')
@ns.response(404, 'Category not found')
@ns.param('category_id', 'List of topics in category')
class TopicListAPI(Resource):
    '''Gets a user'''
    @ns.doc('List Topics')
    @ns.marshal_with(topicListModel)
    def get(self, category_id):
        '''Fetch a given resource'''
        return {"topics" : topic.retrieve_topics(category_id=category_id)}, 201

@ns.route('/')
@ns.response(404, 'Error creating topic')
class CreateTopicAPI(Resource):
    @ns.doc('create_topic')
    @ns.expect(topicModel)
    @ns.marshal_with(topicModel, code=201)
    def post(self):
        '''Create a new topic'''
        return topic.create_topic(type=api.payload["type"], name=api.payload["name"], category_id=api.payload["category_id"]), 201
