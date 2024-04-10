from flask_caching import Cache
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
migrate = Migrate()
cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})
bcrypt = Bcrypt()
