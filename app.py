"""The main Flask app"""
from flask import Flask
from flask_restx import Api
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
    """Enable Cross Origin Resource Sharing"""
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