#!/usr/bin/python3
"""DOCSTRING FOR MODULE"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.place import Place


@app_views.route(
        '/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def show_places(city_id):
    """retrieves all Place objects"""
    city = storage.get('City', city_id)
    places_list = []
    if city is not None:
        for place in city.places:
            places_list.append(place.to_dict())
        return jsonify(places_list)
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def show_place(place_id):
    """retrieves a Place object by place_id"""
    place = storage.get('Place', place_id)
    if place is not None:
        return jsonify(place.to_dict())
    else:
        abort(404)


@app_views.route(
        '/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """deletes a Place object by place_id"""
    place = storage.get('Place', place_id)
    if place is not None:
        storage.delete(place)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route(
        '/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """creates a Place object"""
    city = storage.get('City', city_id)
    if city is not None:
        content = request.get_json(silent=True)
        if type(content) is dict:
            if "user_id" in content.keys():
                user = storage.get('User', content['user_id'])
                if user is not None:
                    if "name" in content.keys():
                        place = Place(**content)
                        place.city_id = city_id
                        storage.new(place)
                        storage.save()
                        response = jsonify(place.to_dict())
                        response.status_code = 201
                        return response
                    else:
                        error_message = "Missing name"
                else:
                    abort(404)
            else:
                error_message = "Missing user_id"
        else:
            error_message = "Not a JSON"
        response = jsonify({"error": error_message})
        response.status_code = 400
        return response
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """updates a Place object"""
    place = storage.get('Place', place_id)
    if place is not None:
        content = request.get_json(silent=True)
        if type(content) is dict:
            ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
            for key, value in content.items():
                if key in ignore:
                    continue
                else:
                    setattr(place, key, value)
            storage.save()
            return jsonify(place.to_dict())
        else:
            response = jsonify({"error": "Not a JSON"})
            response.status_code = 400
            return response
    else:
        abort(404)
