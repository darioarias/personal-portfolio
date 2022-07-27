from datetime import datetime
from peewee import *
from flask import current_app as app
from playhouse.shortcuts import model_to_dict
from .validators import TimelinePostValidator
import os

mydb_proxy = DatabaseProxy()  # Create a proxy for our db.


class TimelinePost(Model):
  name = CharField()
  email = CharField()
  content = TextField()
  created_at = DateTimeField(default=datetime.utcnow)

  class Meta:
    database = mydb_proxy

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
# mydb.connect(reuse_if_open=True)
# mydb.create_tables([TimelinePost])

# dynamically creates the database
if app.config['TESTING']:
  database = SqliteDatabase('test.db', uri=True)  # in memory database
else:
  database = MySQLDatabase(
      os.getenv('MYSQL_DATABASE'),
      user=os.getenv('MYSQL_USER'),
      password=os.getenv('MYSQL_PASSWORD'),
      host=os.getenv('MYSQL_HOST'),
      port=3306
  )  # connects to database

mydb_proxy.initialize(database)
