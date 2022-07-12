from datetime import datetime
from peewee import *
from flask import current_app
from playhouse.shortcuts import model_to_dict
from app import db as mydb
from .validators import TimelinePostValidator
# creating database connection instance


class TimelinePost(Model):
  name = CharField()
  email = CharField()
  content = TextField()
  created_at = DateTimeField(default=datetime.utcnow)

  class Meta:
    database = mydb

  def validate(self):
    validator = TimelinePostValidator(self)
    validator.validate()
    if len(validator.errors) > 0:
      for key in validator.errors:
        validator.errors[key] = f'Invalid {key}'
      return {'valid': False, 'message': validator.errors}
    else:
      return {'valid': True, "message": ""}

  def to_json(self):
    return model_to_dict(self)

# TODO: abstract this logic into a context cli function to create all tables, it will be very helpful when deploying
# mydb.connect();
# mydb.create_tables([TimelinePost])
