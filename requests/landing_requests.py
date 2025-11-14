"""Requests made upon landing in the app after login"""
from flask import Blueprint
from flask_restx import Api, Resource
from control.category_controller import CategoryController
from control.topic_controller import TopicController
from datamodel.message import ApiMessage
from datamodel.topic import ApiTopic




LandingBlueprint = Blueprint('landing', __name__)
api = Api(LandingBlueprint, version='1.0', title='API',
    description='An API',
)
ns = api.namespace('', description='Requests made upon landing in the app after login')
messageModel = ApiMessage(api).get_model()
messagesModel = ApiMessage(api).get_list()
categories = CategoryController()
topics = TopicController()
topicModel = ApiTopic(api).get_model()

# @ns.route('/justlanded')
# @ns.response(404, 'Error Landing')
# class JustLandingAPI(Resource):
#     pass

@ns.route('/generalLanding')
@ns.response(404, 'Error Landing')
class GeneralLandingAPI(Resource):
    """This is for bringing up the general Topic when you login"""
    @ns.doc("Return the General Topic ID")
    @ns.marshal_with(topicModel, code=201)
    def get(self):
        """Return the General Topic ID"""
        general_category = categories.general_landing()
        return topics.general_landing(general_category["_id"])


    