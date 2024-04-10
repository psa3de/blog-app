from flask import request
from flask_restx import Resource
from src.main.controllers.auth_controller import login_user, signup_user

from src.main.views.schemas import (
    login_request,
    signup_request,
    auth_ns as api
)

@api.route('/login')
class UserLogin(Resource):
    @api.doc('login_user')
    @api.expect(login_request, validate=True)
    @api.response(200, 'Successfully logged in.')
    @api.response(400, 'Bad input.')
    @api.response(401, 'Login required.')
    @api.response(403, 'Unable to authenticate.')
    @api.response(500, 'An error occurred.')
    def post(self):
        return login_user(request.json)
    
@api.route('/signup')
class UserSignup(Resource):
    @api.doc('signup_user')
    @api.expect(signup_request, validate=True)
    @api.response(201, 'User successfully registered.')
    @api.response(202, 'User already exists.')
    @api.response(400, 'Bad input.')
    @api.response(409, 'Database conflict.')
    @api.response(500, 'An error occurred.')
    def post(self):
        return signup_user(request.json)
