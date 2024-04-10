from extensions import db
from flask import abort
from sqlalchemy.exc import IntegrityError

from logger import log
from src.main.models.user import User
from src.main.constants import STATUS_ACTIVE, STATUS_DELETED

# Database interactions
def update_db(user: User):
    db.session.add(user)
    db.session.commit()

def update_attributes(user: User, input: dict):
    for key, value in input.items():
        setattr(user, key, value)
    update_db(user)

def create_user_from_dict(input: dict) :
    user = User(
        username = input['username'],
        admin = False,
        status = STATUS_ACTIVE,
        email = input['email']
    )
    user.password_hash = input['password']
    update_db(user)
    log.info('User %s created', user.username)
    return user

def get_users():
    return User.query.all()

def get_user_by_id(user_id: int) -> User:
    return User.query.filter_by(id=user_id).first()

def get_user_by_public_id(public_id: int) -> User:
    return User.query.filter_by(public_id=public_id).first()

def get_user_by_email(email: str) -> User:
    return User.query.filter_by(email=email).first()

# Responses
def update_user(user: User, input: dict):
    try:
        update_attributes(user, input)
    except IntegrityError as e:
        log.error('%s', e.args)
        abort(409, 'Database conflict.')
    except Exception as e:
        log.error('%s', e.args)
        abort(500, 'An error occurred.')
    return user

def delete_user(user: User):
    update_user(user, {'status': STATUS_DELETED})
    log.info('User %s deleted', user.username)

def create_user_response(user_input: dict):
    try:
        new_user = create_user_from_dict(user_input)
    except IntegrityError as e:
        log.error('%s', e.args)
        abort(409, 'Database conflict.')
    except Exception as e:
        log.error('%s', e.args)
        abort(500, 'An error occurred.')
    return new_user, 201
    
def get_user_response(user_id: int):
    try:
        user = get_user_by_id(user_id)
    except Exception as e:
        log.error('%s', e.args)
        abort(500, 'An error occurred.')
    if not user:
        abort(404, 'User not found.')
    return user, 200

def get_users_response():
    try:
        users = get_users()
    except Exception as e:
        log.error('%s', e.args)
        abort(500, 'An error occurred.')
    if not users:
        return [], 204
    return users, 200

def update_user_response(user_id: int, input: dict, current_user: User):
    if not current_user or current_user.id != user_id:
        abort(401, 'Unauthorized.')
    try:
        user = get_user_by_id(user_id)
    except Exception as e:
        log.error('%s', e.args)
        abort(500, 'An error occurred.')
    if not user:
        abort(404, 'User not found.')
    user = update_user(user, input)
    return user, 201
 
def delete_user_response(user_id: int, current_user: User):
    if not current_user or current_user.id != user_id:
        abort(401, 'Unauthorized.')
    try:
        user = get_user_by_id(user_id)
    except Exception as e:
        log.error('%s', e.args)
        abort(500, 'An error occurred.')
    if not user:
        abort(404, 'User not found.')
    delete_user(user)
    return 'User successfully deleted.', 204
