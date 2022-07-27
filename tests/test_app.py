# tests/test_app.py

from app import create_app
from app.models import TimelinePost, database
from playhouse.shortcuts import model_to_dict
import unittest
import os


class AppTestCase(unittest.TestCase):
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
    database.close()

  def test_home(self):
    response = self.client.get("/")
    self.assertEqual(response.status_code, 200)
    html = response.get_data(as_text=True)
    self.assertIn('Welcome to my Portfolio', html)
    # TODO Add more tests relating to the home page
    self.assertIn('Production Engineer', html)
    self.assertIn('<img', html)

  def test_timeline(self):
    response = self.client.get("/api/v1/timeline_post")
    self.assertEqual(response.status_code, 200)
    self.assertTrue(response.is_json)

    json = response.get_json()
    self.assertIn("timeline_posts", json)
    self.assertTrue(len(json["timeline_posts"]) == 0)
    jane_form = {'name': 'Jane', 'email': "jstreet@gmail.com",
                 "content": "jstreet saves you mula :)"}
    john_form = {'name': 'John', 'email': "jsmith@gmail.com",
                 "content": "Hello, this is JSmith"}

    # TODO Add more tests relating to the /api/timeline post GET and POST apis
    # testing posts api
    response = self.client.post('/api/v1/timeline_post', data=jane_form)
    self.assertEqual(response.status_code, 200)
    self.assertTrue(response.is_json)

    jane_json = response.get_json()
    self.assertTrue(jane_json['name'] == 'Jane')
    self.assertTrue(jane_json['email'] == 'jstreet@gmail.com')
    self.assertTrue(jane_json['id'] == 1)

    response = self.client.post('/api/v1/timeline_post', data=john_form)
    self.assertEqual(response.status_code, 200)
    self.assertTrue(response.is_json)

    john_json = response.get_json()
    self.assertTrue(john_json['name'] == 'John')
    self.assertFalse(
        'email' in john_json and john_json['email'] == 'jstreet@gmail.com')
    self.assertTrue(john_json['id'] == 2)

    # testing get api
    response = self.client.get('/api/v1/timeline_post')
    self.assertEqual(response.status_code, 200)
    self.assertTrue(response.is_json)

    posts = response.get_json()
    self.assertIn('timeline_posts', posts)
    self.assertTrue(len(posts['timeline_posts']) == 2)

    # TODO Add more tests relating to the timeline page
    response = self.client.get('/timeline')
    self.assertEqual(response.status_code, 200)

    html = response.get_data(as_text=True)
    self.assertIn('">Jane</a>', html)
    self.assertIn('">John</a>', html)
    self.assertIn('submit', html)

  def test_malformed_timeline_post(self):
    # POST request missing name
    response = self.client.post(
        "/api/v1/timeline_post", data={"email": "john@example.com", "content": "Hello world, I'm John!"})
    self.assertEqual(response.status_code, 400)

    html = response.get_data(as_text=True)
    self.assertIn("Invalid name", html)

    # POST request with empty content
    response = self.client.post(
        "/api/v1/timeline_post", data={"name": "John Doe", "email": "john@example.com", "content": ""})
    self.assertEqual(response.status_code, 400)

    html = response.get_data(as_text=True)
    self.assertIn("Invalid content", html)

    # POST request with malformed email
    response = self.client.post("/api/v1/timeline_post", data={
                                "name": "John Doe", "email": "not-an-email", "content": "Hello world, I'm John!"})
    self.assertEqual(response.status_code, 400)
    html = response.get_data(as_text=True)
    self.assertIn("Invalid email", html)
