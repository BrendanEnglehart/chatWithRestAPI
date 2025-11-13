from flask import Blueprint
from flask_restx import Api, Resource

from datamodel.category import ApiCategory
from control.category_controller import CategoryController

CategoryBlueprint = Blueprint('category', __name__)
api = Api(CategoryBlueprint, version='1.0', title='API',
    description='An API',
)
ns = api.namespace('category', description='category Logic')

categoryModel = ApiCategory(api).get_model()
categoriesModel = ApiCategory(api).get_list()
category = CategoryController()

@ns.route('/')
@ns.response(404, 'Error creating category')
class CreateCategoryAPI(Resource):
    """API for creating the category, which is used as a set of Topics"""
    @ns.doc('create_category')
    @ns.expect(categoryModel)
    @ns.marshal_with(categoryModel, code=201)
    def post(self):
        '''Create a new category'''
        return category.create_category( name=api.payload["name"],
                                        joinable=api.payload["joinable"]), 201

    @ns.doc('list_categories')
    @ns.marshal_with(categoriesModel, code=201)
    def get(self):
        '''List Categories'''
        return {"categories" : category.list_categories()}, 201
