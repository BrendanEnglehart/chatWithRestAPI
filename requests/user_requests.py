from flask import Blueprint
from flask_restx import Api, Resource

from control.user_controller import user_controller
from flask import Blueprint
from flask_restx import Api, Resource

from datamodel.user import ApiUser, ReturnUser



bp = Blueprint('user', __name__)
api = Api(bp, version='1.0', title='API',
    description='An API',
)
ns = api.namespace('', description='User Logic')

users = user_controller()
recieveUserModel = ApiUser(api).Model()
returnUserModel = ReturnUser(api).Model()



@ns.route('/')
class UserAPI(Resource):
    @ns.doc('create_user')
    @ns.expect(recieveUserModel)
    @ns.marshal_with(returnUserModel, code=201)
    def post(self):
        '''Create a new user'''
        return users.create_user(username=api.payload["username"], picture=api.payload["picture"], email=api.payload["email"]), 201

@ns.route('/<string:username>')
@ns.response(404, 'Username not found')
@ns.param('username', 'The username to retrieve')
class UserGetAPI(Resource):
    '''Gets a user'''
    @ns.doc('get_user')
    @ns.marshal_with(returnUserModel)
    def get(self, username):
        '''Fetch a given resource'''
        return users.get_user(username=username)