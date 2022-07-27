from app import create_app
import os
# from app import db
# from app.models import TimelinePost
import click
from flask import current_app

app = create_app(config_profile=os.getenv('FLASK_CONFIG') or 'development')


@app.shell_context_processor
def make_shell_context():
  print('making context')
  with app.app_context():
    from app.models import TimelinePost
    return dict(app=app, TimelinePost=TimelinePost)


@app.cli.command()
def deploy():
  print('Deploying db')
  # with db.connection_context():
  #   db.create_tables([TimelinePost])
  with current_app.app_context():
    from app.models import database as db, TimelinePost
    db.connect(reuse_if_open=True)
    db.create_tables([TimelinePost], safe=True)


@app.cli.command()
@click.argument('test_names', nargs=-1)
def test(test_names):
  # if app.config[]
  # app.app_context().pop()
  import unittest
  if test_names:
    tests = unittest.TestLoader().loadTestsFromNames(
        names=[f'tests.{test}' for test in test_names])
  else:
    tests = unittest.TestLoader().discover('tests')

  unittest.TextTestRunner(verbosity=2).run(test=tests)
  # sys.exit(not result.wasSuccessful())
