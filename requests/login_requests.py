from flask import Blueprint
from flask_restx import Api, Resource

from control.session_controller import session_controller
from control.user_controller import user_controller
from flask import Blueprint
from flask_restx import Api, Resource

from datamodel.session import ApiSession
from datamodel.user import ApiUser



bp = Blueprint('login', __name__)
api = Api(bp, version='1.0', title='API',
    description='An API',
)
ns = api.namespace('', description='login Logic')

users = user_controller()
recieveUserModel = ApiUser(api).Model()
sessionUserModel = ApiSession(api).Model()
# The Operations on Session table in the chat database
session = session_controller()



# Deprecated now that Auth0 has been implemented
@ns.route('/')
class UserGetAPI(Resource):
    '''login a user'''
    @ns.doc('login')
    @ns.expect(recieveUserModel)
    @ns.marshal_with(sessionUserModel, code=201)
    def post(self):
        '''Create a new user'''
        if (users.login(username=api.payload["username"], picture=api.payload["picture"])):
            return session.create_session(api.payload["username"])
        else:
            api.abort(404, "error")