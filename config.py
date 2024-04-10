class Config(object):
    DEBUG = True
    SECRET_KEY = 'my_secret'
    SQLALCHEMY_DATABASE_URI = 'database_uri'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:admin@blog-app_db_1:3306/blog?auth_plugin=mysql_native_password'

config_map = {
    'dev': DevelopmentConfig,
    'test': TestingConfig
}
