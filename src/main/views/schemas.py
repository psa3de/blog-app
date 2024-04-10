from flask_restx import Namespace, fields

# USERS
user_ns = Namespace('user', description='User operations')
create_user_request = user_ns.model('CreateUserRequest', {
    'username': fields.String(required=True, description='Username'),
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password'),
  },
  strict=True
)
update_user_request = user_ns.model('UpdateUserRequest', {
    'username': fields.String(required=False, description='Username'),
    'password': fields.String(required=False, description='User password'),
  },
  strict=True
)
user_response = user_ns.model('UserResponse', {
    'id': fields.String(required=True, description='Unique user id'),
    'username': fields.String(required=True, description='Username'),
    'email': fields.String(required=True, description='User email'),
  }
)

# AUTH
auth_ns = Namespace('auth', description='Auth operations')
login_request = auth_ns.model('LoginRequest', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password'),
  },
  strict=True
)
signup_request = auth_ns.model('SignupRequest', {
    'username': fields.String(required=True, description='Username'),
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password'),
  },
  strict=True
)

# POSTS
post_ns = Namespace('post', description='Blog post operations')
post_request = post_ns.model('PostRequest', {
    'title': fields.String(required=True, description='Post title'),
    'content': fields.String(required=True, description='Post content'),
  },
  strict=True
)
post_response = post_ns.model('PostResponse', {
    'id': fields.String(required=True, description='Unique user id'),
    'author_id': fields.String(required=True, description='Post author'),
    'title': fields.String(required=True, description='Post title'),
    'content': fields.String(required=True, description='Post content'),
    'status': fields.String(required=True, description='Post status'),
  }
)
