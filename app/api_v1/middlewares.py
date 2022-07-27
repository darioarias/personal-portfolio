from . import api_v1
from flask import current_app as app


@api_v1.before_request
def before_request():
  with app.app_context():
    from app.models import database
    database.connect(reuse_if_open=True)


@api_v1.after_request
def after_request(response):
  with app.app_context():
    from app.models import database
    database.close()
  return response
