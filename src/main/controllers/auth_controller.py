
from datetime import datetime, timedelta, timezone
from flask import abort, current_app, Response
import json
import jwt

from logger import log
from src.main.controllers.user_controller import create_user_response, get_user_by_email

def get_secret():
    return current_app.config['SECRET_KEY']

def login_user(auth: dict) -> Response:
    if not auth or not auth.get('email') or not auth.get('password'):
        abort(401, 'Login required.')

    user = get_user_by_email(auth.get('email'))
  
    if not user:
        abort(401, 'User does not exist.')

    if not user.authenticate(auth.get('password')):
        abort(403, 'Wrong password.')

    token = jwt.encode({
        'public_id': user.public_id,
        'exp' : datetime.now(timezone.utc) + timedelta(minutes = 30)
    }, get_secret())

    log.info('User %s logged in', user.username)
    response = json.dumps({'token' : token})
    return response, 200

def signup_user(input: dict) -> Response:
    user = get_user_by_email(input.get('email'))
    
    if user:
        return 'User already exists.', 202
    
    create_user_response(input)
    return 'User successfully registered.', 201
