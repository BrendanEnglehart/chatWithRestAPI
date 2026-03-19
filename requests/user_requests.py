"""
User Request Handler
Most User Requests will be changed with the new Auth
"""

from flask import Blueprint
from flask_restx import Api, Resource

from control.user_controller import UserController
from datamodel.user import ApiUser, ReturnUser


bp = Blueprint("user", __name__)
api = Api(
    bp,
    version="1.0",
    title="API",
    description="An API",
)
ns = api.namespace("", description="User Logic")

users = UserController()
recieveUserModel = ApiUser(api).get_model()
returnUserModel = ReturnUser(api).get_model()


@ns.route("/login")
class UserAPI(Resource):
    """Create a User"""

    @ns.doc("create_user")
    @ns.expect(recieveUserModel)
    @ns.marshal_with(returnUserModel, code=201)
    def post(self):
        """Create a new user"""
        return (
            users.create_or_retrieve_user(
                {
                    "username": api.payload["username"],
                    "picture": api.payload["picture"],
                    "email": api.payload["email"],
                    "auth_id": api.payload["auth_id"],
                }
            ),
            201,
        )


@ns.route("/update_username")
class UpdateUsername(Resource):
    """Update Username"""

    @ns.doc("update_username")
    @ns.expect(returnUserModel)
    @ns.marshal_with(bool, code=201)
    def post(self):
        """update username"""
        return (
            users.update_username(
                username=api.payload["username"],
                user_id=api.payload["_id"],
            ),
            201,
        )
