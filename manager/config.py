import os

from werkzeug.utils import import_string

CONFIG_NAME_MAPPER = {
    'development': 'config.DevelopmentConfig'
}


def get_config(config_name=None):
    flask_config_name = os.getenv('FLASK_CONFIG', 'development')
    if config_name is not None:
        flask_config_name = config_name
    return import_string(CONFIG_NAME_MAPPER[flask_config_name])


class BaseConfig:
    DEVELOPMENT = False
    DOMAIN = 'http://localhost:5000'
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % (
        os.path.join(PROJECT_ROOT, "db.sqlite3"))
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class DevelopmentConfig(BaseConfig):
    ENV = 'development'
    DEVELOPMENT = True
