from flask import request
from flask_restx import Resource

from src.main.views.decorators import jwt_required
from src.main.controllers.post_controller import (
    create_post_response,
    delete_post_response,
    get_post_response,
    get_posts_response,
    update_post_response
)
from src.main.views.schemas import (
    post_request,
    post_response,
    post_ns as api
)

@api.route('/')
class PostList(Resource):
    @api.doc('list_posts')
    @api.marshal_list_with(post_response)
    @api.response(200, 'Posts fetched successfully.')
    @api.response(204, 'No posts found.')
    @api.response(500, 'An error occurred.')
    def get(self):
        return get_posts_response()

    @api.doc('create_post')
    @api.expect(post_request, validate=True)
    @api.marshal_with(post_response)
    @api.response(201, 'User created successfully.')
    @api.response(400, 'Bad input.')
    @api.response(401, 'Unauthorized.')
    @api.response(500, 'An error occurred.')
    @jwt_required
    def post(self, current_user):
        return create_post_response(request.json, current_user)
    
@api.route('/<int:id>')
class Post(Resource):
    @api.doc('get_post')
    @api.marshal_with(post_response)
    @api.response(200, 'Post fetched successfully.')
    @api.response(404, 'Post not found.')
    @api.response(500, 'An error occurred.')
    def get(self, id):
        return get_post_response(id)

    @api.doc('edit_post')
    @api.expect(post_request, validate=True)
    @api.marshal_with(post_response)
    @api.response(201, 'Post updated successfully.')
    @api.response(400, 'Bad input.')
    @api.response(401, 'Unauthorized.')
    @api.response(404, 'User not found.')
    @api.response(500, 'An error occurred.')
    @jwt_required
    def put(self, id, current_user):
        return update_post_response(id, request.json, current_user)
    
    @api.doc('delete_post')
    @api.response(204, 'Post deleted successfully.')
    @api.response(401, 'Unauthorized.')
    @api.response(404, 'User not found.')
    @api.response(500, 'An error occurred.')
    @jwt_required
    def delete(self, id, current_user):
        return delete_post_response(id, current_user)
