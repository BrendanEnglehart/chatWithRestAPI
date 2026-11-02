"""Request handler for the Topic section of the API"""

from flask import Blueprint, request
from flask_restx import Api, Resource
from datamodel.topic import ApiTopic
from control.topic_controller import TopicController

PrivateBlueprint = Blueprint("Private", __name__)  # pylint: disable=invalid-name
api = Api(
    PrivateBlueprint,
    version="1.0",
    title="API",
    description="An API",
)
ns = api.namespace("", description="Private topic Logic")

topicModel = ApiTopic(api).get_model()
topicListModel = ApiTopic(api).get_list()
topic = TopicController()

@ns.route("/create_or_retrieve_private_chat")
@ns.response(404, "Category not found")
@ns.param("users", "List of users for private chat")
class CreatePrivateMessageTopicAPI(Resource):
    """Gets a Topic, which contains metadata for displaying chat data"""

    @ns.doc("Create or retrieve private chat Topics")
    @ns.marshal_with(topicModel)
    def get(self):
        """Returns a direct Message Topic"""
        return (
            topic.direct_message_topic(user_id_list=request.args.get("users", "").split(",")),
            201,
        )