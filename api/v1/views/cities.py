#!/usr/bin/python3
"""DOCSTRING FOR MODULE"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.city import City
from models.state import State


@app_views.route(
        '/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def show_cities(state_id):
    """shows all City objects that are associated with a State object"""
    city_list = []
    state = storage.get("State", state_id)
    if state is not None:
        for city in state.cities:
            city_list.append(city.to_dict())
        return jsonify(city_list)

    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def show_city(city_id):
    """shows a City object by the city_id"""
    city = storage.get("City", city_id)
    if city is not None:
        return jsonify(city.to_dict())
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """deletes a City object"""
    city = storage.get("City", city_id)
    if city is not None:
        storage.delete(city)
        storage.save()
        response = jsonify({})
        response.status_code = 200
        return response
    else:
        abort(404)


@app_views.route(
        '/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """creates a City object"""
    error_message = ""
    state = storage.get("State", state_id)
    if state is not None:
        content = request.get_json(silent=True)
        if type(content) is dict:
            if "name" in content.keys():
                city = City(**content)
                setattr(city, "state_id", state_id)
                storage.new(city)
                storage.save()
                response = jsonify(city.to_dict())
                response.status_code = 201
                return response
            else:
                error_message = "Missing name"
        else:
            error_message = "Not a JSON"
        response = jsonify({"error": error_message})
        response.status_code = 400
        return response
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """updates a City object"""
    ignore = ['id', 'state_id', 'created_at', 'updated_at']
    city = storage.get("City", city_id)
    if city is not None:
        content = request.get_json(silent=True)
        if type(content) is dict:
            for key, value in content.items():
                if key not in ignore:
                    setattr(city, key, value)
            storage.save()
            response = jsonify(city.to_dict())
            response.status_code = 200
            return response
        else:
            response = jsonify({"error": "Not a JSON"})
            response.status_code = 400
            return response
    else:
        abort(404)
