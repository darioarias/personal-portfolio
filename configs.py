import secrets
import os
from peewee import *
from dotenv import load_dotenv
load_dotenv()


class Config:
  SECRET_KEY = secrets.token_hex(255)  # creates app's secret key
  FLASK_COVERAGE = False  # Sets Coverage for unit testing and for testing coverage
  DB_URL = os.getenv('DB_URL')
  MYSQL_HOST = os.getenv('MYSQL_HOST')
  MYSQL_USER = os.getenv('MYSQL_USER')
  MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
  MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')

  @staticmethod
  def init_app(app):
    pass


class DevelopmentConfig(Config):
  DEBUG = True  # enables debug mode
  SQLALCHEMY_TRACK_MODIFICATIONS = True
  MYSQL_HOST = "localhost"

  @classmethod
  def init_app(cls, app):
    pass

    # check for settings


class ProductionConfig(Config):
  DEBUG = False  # enables debug mode
  FLASK_COVERAGE = False

  @classmethod
  def init_app(cls, app):
    pass


class TestingConfig(Config):
  TESTING = True
  WTF_CSRF_ENABLED = False

  @classmethod
  def init_app(cls, app):
    pass


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
