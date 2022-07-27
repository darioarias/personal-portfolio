from flask import Flask
from configs import config
from flask_bootstrap import Bootstrap
import os
from peewee import *
from flask_moment import Moment

bootstrap = Bootstrap()
moment = Moment()


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
    from .api_v1 import api_v1 as api_v1_blueprint
    app.register_blueprint(api_v1_blueprint, url_prefix='/api/v1')

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

  # returns app instance
  return app
