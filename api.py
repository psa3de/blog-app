from flask import Blueprint
from flask_restx import Api

from src.main.views.auth_routing import api as auth_ns
from src.main.views.post_routing import api as post_ns
from src.main.views.user_routing import api as user_ns

blueprint = Blueprint('api', __name__, url_prefix='/api/v1')

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

api = Api(blueprint,
          title='Blog API',
          version='1.0',
          description='API for blogs',
          authorizations=authorizations,
          security='apikey')

api.add_namespace(user_ns, path='/user')
api.add_namespace(auth_ns, path='/auth')
api.add_namespace(post_ns, path='/post')
