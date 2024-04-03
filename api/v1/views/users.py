#!/usr/bin/python3
"""TODO"""

from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users():
    """Retrieves all users as json objects."""
    all_users = []
    for user in storage.all('User').values():
        all_users.append(user.to_dict())
    return jsonify(all_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Retrieves a specific User object by user_id, else 404s."""
    user = storage.get('User', user_id)
    if user is None:
        abort(404)
    else:
        return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """
    Deletes a specific User object by user_id.
    Returns an empty dictionary with the status code 200, else 404s.
    """
    user = storage.get('User', user_id)
    if user is None:
        abort(404)
    else:
        storage.delete(user)
        storage.save()
        return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """
    Creates a new User object by user_id.
    Returns a user dictionary with the status code 201, else 400 w/ message.
    """
    err_msg = ""
    user_json = request.get_json()
    if user_json is None:
        err_msg = "Not a JSON"
    else:
        if 'email' not in user_json.keys():
            err_msg = "Missing email"
        if 'password' not in user_json.keys():
            err_msg = "Missing password"
    if err_msg != "":
        return make_response(jsonify({"error": err_msg}), 400)
    else:
        new_user = User(**user_json)
        storage.new(new_user)
        storage.save()
        return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Updates a specific User object by user_id, else 404s."""
    ignore = ['id', 'email', 'created_at', 'updated_at']
    user = storage.get('User', user_id)
    if user is None:
        abort(404)
    json_dict = request.get_json()
    if json_dict is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for key, value in json_dict.items():
        if key not in ignore:
            setattr(user, key, value)
    storage.new(user)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
