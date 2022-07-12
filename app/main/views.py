from . import main
from .forms import TimelinePostForm
from flask import render_template, abort, url_for, redirect, send_file, jsonify
from app.models import TimelinePost


@main.route('/')
def index():
  return render_template("index.html")


@main.route('/timeline', methods=['GET', "POST"])
def timeline():
  form = TimelinePostForm()
  if form.validate_on_submit():
    post = TimelinePost(name=form.name.data,
                        email=form.email.data, content=form.content.data)
    try:
      post.save()
    except:
      return abort(422)
    return redirect(url_for('main.timeline'))
  posts = TimelinePost.select().order_by(TimelinePost.created_at.desc())
  return render_template('timeline.html', form=form, timeline_events=[post for post in posts])


@main.route('/projects')
def projects():
  return render_template('projects.html')


@main.route('/resources/<string:resource>')
def resources(resource: str = None):
  if resource is not None and resource.lower() == 'map':
    return send_file('templates/maps/dario-places-visited.html')
  return jsonify({"message": "resource not found"}), 404


@main.route('/ph/<string:size>')
def placeholder(size=None):
  if size.lower() == 'large':
    return render_template("base-large.html")
  return render_template("base.html")


@main.route('/v2/', defaults={'path': ''})
@main.route('/v2/<path:path>')
def redirect_(path):
  return redirect(url_for('main.index')), 302
