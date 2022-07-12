from flask import Flask
from configs import config
from flask_bootstrap import Bootstrap
import os
from peewee import *
from flask_moment import Moment

bootstrap = Bootstrap()
moment = Moment()
db = Proxy()  # Create a proxy for our db.


def create_app(config_profile: str):
  # creates app instance
  app = Flask(__name__)
  app.config.from_object(config[config_profile])
  config[config_profile].init_app(app)

  # init plug ins
  bootstrap.init_app(app)
  moment.init_app(app)
  # db.init_app(app)

  # loads the view(s)
  with app.app_context():
    from . import models

    from .api_v1 import api_v1 as api_v1_blueprint
    app.register_blueprint(api_v1_blueprint, url_prefix='/api/v1')

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

  if app.config['TESTING']:
    print('CREATING TESTING DATABASE')
    database = SqliteDatabase(
        'file:memory?mode=memory&cache=shared', uri=False)
  else:
    database = MySQLDatabase(
        os.getenv('MYSQL_DATABASE'),
        user=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD'),
        host=os.getenv('MYSQL_HOST'),
        port=3306
    )
  db.initialize(database)

  # returns app instance
  return app
