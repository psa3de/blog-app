from extensions import db, cache
from flask import abort
from logger import log
from sqlalchemy.exc import IntegrityError

from src.main.models.post import Post
from src.main.models.user import User
from src.main.constants import STATUS_LIVE, STATUS_DELETED

# Database interactions
def update_db(post: Post):
    db.session.add(post)
    db.session.commit()

def update_attributes(post: Post, input: dict):
    for key, value in input.items():
        setattr(post, key, value)
    update_db(post)

def create_post_from_dict(input: dict) :
    post = Post(
        title = input['title'],
        author_id = input['author_id'],
        content = input['content'],
        status = STATUS_LIVE
    )
    update_db(post)
    log.info('Post %s created', post.title)
    return post

def get_posts():
    return Post.query.all()

def get_post_by_id(post_id: int) -> Post:
    return Post.query.filter_by(id=post_id).first()

@cache.memoize(60)
def get_user_posts(user_id: int):
    return Post.query.filter_by(author_id=user_id).all()

# Responses
def update_post(post: Post, input: dict):
    try:
        update_attributes(post, input)
    except IntegrityError as e:
        log.error('%s', e.args)
        abort(409, 'Database conflict.')
    except Exception as e:
        log.error('%s', e.args)
        abort(500, 'An error occurred.')
    return post

def delete_post(post: Post):
    update_post(post, {'status': STATUS_DELETED})
    log.info('Post %s deleted', post.title)

def create_post_response(post_input: dict, current_user: User):
    if not current_user:
        abort(401, 'Unauthorized.')
    try:
        post_input['author_id'] = current_user.id
        new_post = create_post_from_dict(post_input)
    except Exception as e:
        log.error('%s', e.args)
        abort(500, 'An error occurred.')
    cache.delete_memoized(get_user_posts, current_user.id)
    return new_post, 201
    
def get_post_response(post_id: int):
    try:
        post = get_post_by_id(post_id)
    except Exception as e:
        log.error('%s', e.args)
        abort(500, 'An error occurred.')
    if not post:
        abort(404, 'Post not found.')
    return post, 200

def get_posts_response():
    try:
        posts = get_posts()
    except Exception as e:
        log.error('%s', e.args)
        abort(500, 'An error occurred.')
    if not posts:
        return [], 204
    return posts, 200

def get_user_posts_response(user_id: int):
    try:
        posts = get_user_posts(user_id)
    except Exception as e:
        log.error('%s', e.args)
        abort(500, 'An error occurred.')
    if not posts:
        return [], 204
    return posts, 200

def update_post_response(post_id: int, input: dict, current_user: User):
    try:
        post = get_post_by_id(post_id)
    except Exception as e:
        log.error('%s', e.args)
        abort(500, 'An error occurred.')
    if not post:
        abort(404, 'Post not found.')
    if not current_user or current_user.id != post.author_id:
        abort(401, 'Unauthorized.')
    post = update_post(post, input)
    cache.delete_memoized(get_user_posts, current_user.id)
    return post, 201
 
def delete_post_response(post_id: int, current_user: User):
    try:
        post = get_post_by_id(post_id)
    except Exception as e:
        log.error('%s', e.args)
        abort(500, 'An error occurred.')
    if not post:
        abort(404, 'Post not found.')
    if not current_user or current_user.id != post.author_id:
        abort(401, 'Unauthorized.')
    delete_post(post)
    cache.delete_memoized(get_user_posts, current_user.id)
    return 'Post successfully deleted.', 204
