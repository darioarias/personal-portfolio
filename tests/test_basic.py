import unittest
from app.models import TimelinePost, database
from flask import current_app
from app import create_app
import os


class BasicTests(unittest.TestCase):
  """ This unit test is mean to test basic parts of the app, checking that all endpoints respond with no error code """
  @classmethod
  def tearDownClass(cls):
    os.system('rm -f test.db')

  def setUp(self):
    self.app = create_app('testing')
    self.app_context = self.app.app_context()
    self.app_context.push()
    self.client = self.app.test_client()

    database.connect(reuse_if_open=True)
    database.create_tables([TimelinePost], safe=True)

  def tearDown(self):
    self.app_context.pop()

  def test_app_runs(self):
    self.assertFalse(current_app is None)

  def test_landing_page_is_up(self):
    response = self.client.get('/')
    self.assertEqual(response.status_code, 200)

  def test_timeline_page_is_up(self):
    response = self.client.get('/timeline')
    self.assertEqual(response.status_code, 200)

  def test_projects_page_is_up(self):
    response = self.client.get('/projects')
    self.assertEqual(response.status_code, 200)
