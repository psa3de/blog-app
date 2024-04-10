from flask_restx import Resource 
from flask import request

from src.main.controllers.post_controller import get_user_posts_response
from src.main.controllers.user_controller import (
    get_users_response,
    get_user_response,
    delete_user_response,
    update_user_response,
    create_user_response
)

from src.main.views.decorators import admin_required, jwt_required

from src.main.views.schemas import (
    create_user_request,
    update_user_request,
    user_response,
    post_response,
    user_ns as api
)

@api.route('/')
class UserList(Resource):
    @api.doc('create_user')
    @api.expect(create_user_request, validate=True)
    @api.marshal_with(user_response, code=201)
    @api.response(201, 'User created successfully.')
    @api.response(400, 'Bad input.')
    @api.response(401, 'Unauthorized.')
    @api.response(403, 'Forbidden.')
    @api.response(409, 'Database conflict.')
    @api.response(500, 'An error occurred.')
    @admin_required
    def post(self, current_user):
        return create_user_response(request.json)

    @api.doc('list_users')
    @api.marshal_list_with(user_response)
    @api.response(200, 'Users fetched successfully.')
    @api.response(204, 'No users found.')
    @api.response(401, 'Unauthorized.')
    @api.response(403, 'Forbidden.')
    @api.response(500, 'An error occurred.')
    @admin_required
    def get(self, current_user):
        return get_users_response()
    
@api.route('/<int:id>')
class User(Resource):
    @api.doc('get_user')
    @api.marshal_with(user_response)
    @api.response(200, 'User fetched successfully.')
    @api.response(401, 'Unauthorized.')
    @api.response(404, 'User not found.')
    @api.response(500, 'An error occurred.')
    @admin_required
    def get(self, id, current_user):
        return get_user_response(id)

    @api.doc('update_user')
    @api.expect(update_user_request, validate=True)
    @api.marshal_with(user_response, code=201)
    @api.response(201, 'User updated successfully.')
    @api.response(400, 'Bad input.')
    @api.response(401, 'Unauthorized.')
    @api.response(404, 'User not found.')
    @api.response(409, 'Database conflict.')
    @api.response(500, 'An error occurred.')
    @jwt_required
    def put(self, id, current_user):
        return update_user_response(id, request.json, current_user)
    
    @api.doc('delete_user')
    @api.response(204, 'User deleted successfully.')
    @api.response(401, 'Unauthorized.')
    @api.response(404, 'User not found.')
    @api.response(500, 'An error occurred.')
    @jwt_required
    def delete(self, id, current_user):
        return delete_user_response(id, current_user)

@api.route('/<int:id>/posts')
class UserPosts(Resource):
    @api.doc('get_user_posts')
    @api.marshal_list_with(post_response)
    @api.response(200, 'User posts fetched successfully.')
    @api.response(204, 'No posts found.')
    @api.response(404, 'User not found.')
    @api.response(500, 'An error occurred.')
    def get(self, id):
        return get_user_posts_response(id)
