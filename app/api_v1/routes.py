from flask import jsonify
from . import api_v1
from app.models import TimelinePost
from flask import request


@api_v1.route('/timeline_post', methods=['POST'])
def post_time_line_post():
  post = TimelinePost(**request.form)

  result = post.validate()
  if not result['valid']:
    return jsonify(result['message']), 400

  try:
    post.save()
    return jsonify(post.to_json())
  except Exception as err:
    print('err', err)
    return jsonify({"message": "unable to create post"}), 500


@api_v1.route('/timeline_post', methods=['GET'])
def get_time_line_post():
  query = TimelinePost.select()
  return jsonify(
      {
          "timeline_posts": [record.to_json() for record in query]
      }
  )


@api_v1.route('/timeline_post/<int:id>', methods=['DELETE'])
def delete_time_line_post(id):
  try:
    post = TimelinePost.get(TimelinePost.id == id)
    rows = post.delete_instance()
    return jsonify({'message': f'post has been deleted', 'meta': f'rows affected: {rows}'})
  except:
    return jsonify({'message': 'unable to delete post'}), 422
