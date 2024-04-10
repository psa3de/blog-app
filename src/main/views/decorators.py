from flask import abort, current_app, request
from functools import wraps
import jwt

from src.main.controllers.user_controller import get_user_by_public_id
from src.main.models.user import User

def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user = get_user_from_token()
        if not user:
            abort(401, 'Token is missing or invalid.')
        kwargs['current_user'] = user
        return  f(*args, **kwargs)
  
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user = get_user_from_token()
        if not user:
            abort(401, 'Token is missing or invalid.')
        if not user.admin:
            abort(403, 'User is not an admin.')
        kwargs['current_user'] = user
        return f(*args, **kwargs)
    return decorated

def get_user_from_token() -> User:
    token = None
    if 'Authorization' in request.headers:
        token = request.headers['Authorization']
    if not token:
        return None
    try:
        data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        current_user = get_user_by_public_id(data['public_id'])
    except:
        return None
    return current_user
