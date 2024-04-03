#!/usr/bin/python3
"""DOCSTRING FOR MODULE"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities/', methods=['GET'], strict_slashes=False)
def show_amenities():
    """retrieves list of all Amenity objects"""
    amenities = list(storage.all('Amenity').values())
    amenities_list = []
    for amenity in amenities:
        amenities_list.append(amenity.to_dict())
    return jsonify(amenities_list)


@app_views.route(
        '/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """retrieves a Amenity object by amenity_id"""
    amenity = storage.get('Amenity', amenity_id)
    if amenity is not None:
        return jsonify(amenity.to_dict())
    else:
        abort(404)


@app_views.route(
        '/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """deletes a Amenity object by amenity_id"""
    amenity = storage.get('Amenity', amenity_id)
    if amenity is not None:
        storage.delete(amenity)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route('/amenities/', methods=['POST'], strict_slashes=False)
def create_amenity():
    """creates a Amenity object"""
    content = request.get_json(silent=True)
    error_message = ""
    if type(content) is dict:
        if "name" in content.keys():
            amenity = Amenity(**content)
            storage.new(amenity)
            storage.save()
            response = jsonify(amenity.to_dict())
            response.status_code = 201
            return response
        else:
            error_message = "Missing name"
    else:
        error_message = "Not a JSON"
    response = jsonify({"error": error_message})
    response.status_code = 400
    return response


@app_views.route(
        '/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """updates a Amenity object"""
    amenity = storage.get('Amenity', amenity_id)
    if amenity is not None:
        content = request.get_json(silent=True)
        if type(content) is dict:
            ignore = ['id', 'created_at', 'updated_at']
            for key, value in content.items():
                if key not in ignore:
                    setattr(amenity, key, value)
            storage.save()
            return jsonify(amenity.to_dict())
        else:
            error_message = "Not a JSON"
            response = jsonify({"error": error_message})
            response.status_code = 400
            return response
    else:
        abort(404)
