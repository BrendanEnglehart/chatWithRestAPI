from flask import Flask
from flask_restx import Api, Resource
from control.user_controller import user_controller
from control.message_controller import message_controller
from datamodel.user import ApiUser, ReturnUser
from flask_cors import CORS
from control.session_controller import session_controller
from datamodel.session import ApiSession
from datamodel.message import ApiMessage
from database.mongodb_connection import mongodb_connection
from requests.message_requests import bp as message_api
from requests.topic_requests import TopicBlueprint
from requests.category_requests import CategoryBlueprint
from requests.user_requests import bp as user_api
from requests.login_requests import bp as login_api


app = Flask(__name__)
app.register_blueprint(message_api, url_prefix="/message")
app.register_blueprint(user_api, url_prefix="/user")
app.register_blueprint(login_api, url_prefix="/login")
# New name conventions, this is more descriptive of what this is doing
app.register_blueprint(TopicBlueprint, url_prefix="/topic")
app.register_blueprint(CategoryBlueprint, url_prefix="/category")

@app.after_request
def enable_cors(response):
    response.headers.add("Access-Control-Allow-Headers", "Access-Control-Allow-Headers, Origin,Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers")
    response.headers.add("Access-Control-Allow-Methods", "DELETE, GET, HEAD, OPTIONS, PATCH, POST, PUT")
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response
api = Api(app, version='1.0', title='API',
    description='An API',
)
ns = api.namespace('chat', description='Chat operations')










#These need new class names, but not now
# @ns.route('/users')
# class UsersAPI(Resource):
#     '''get all users'''
#     @ns.doc('list_users')
#     def get(self):
#         '''List all users'''
#         return users.get_users()

if __name__ == '__main__':
    app.run(debug=True)
else:
    gunicorn = app