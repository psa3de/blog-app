import os

from flask import Flask
from flask_cors import CORS

from api import blueprint as blueprint_v1
import config
from extensions import db, migrate, cache, bcrypt

def create_app():
    flask_app = Flask(__name__)
    environment = os.environ.get('BLOG_APP_ENV', 'test')
    flask_app.config.from_object(config.config_map[environment])
    register_extensions(flask_app)
    register_blueprints(flask_app)
    return flask_app

def register_extensions(flask_app: Flask):
    db.init_app(flask_app)
    cache.init_app(flask_app)
    migrate.init_app(flask_app, db)
    bcrypt.init_app(flask_app)
    CORS(flask_app)

def register_blueprints(flask_app: Flask):
    flask_app.register_blueprint(blueprint_v1)

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
