#!/usr/bin/python3
"""HTTP methods for city  """

from api.v1.views import app_views
from models import storage
from flask import Flask, jsonify, abort, request
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False,  methods=['GET'])
def cities_from_state(state_id=None):
    """  list of all City objects of a State """
    id_state = storage.get('State', state_id)
    if id_state:
        list_cities = []
        for city in id_state.cities:
            list_cities.append(city.to_dict())
        return (jsonify(list_cities))
    else:
        abort(404)


@app_views.route('/cities/<city_id>', strict_slashes=False,  methods=['GET'])
def get_city(city_id=None):
    """ Retrieves a City object """
    id_city = storage.get('City', city_id)
    if id_city:
        return (jsonify(id_city.to_dict()))
    else:
        abort(404)


@app_views.route('/cities/<city_id>',
                 strict_slashes=False,
                 methods=['DELETE'])
def delete_city(city_id=None):
    """Deletes a city object"""
    id_city = storage.get('City', city_id)
    if id_city:
        storage.delete(id_city)
        storage.save()
        return (jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False,  methods=['POST'])
def post_city(state_id=None):
    """ Creates a City """
    id_state = storage.get('State', state_id)
    if id_state is None:
        abort(404)

    dict_request = request.get_json()
    if dict_request is None:
        return (jsonify({'error': 'Not a JSON'}), 400)

    if 'name' not in dict_request:
        return (jsonify({'error': 'Missing name'}), 400)

    dict_request['state_id'] = state_id

    new_obj = City(**dict_request)
    new_obj.save()
    return (jsonify(new_obj.to_dict()), 201)


@app_views.route('cities/<city_id>', strict_slashes=False, methods=['PUT'])
def put_city(city_id=None):
    """ Updates a city """
    update_dict = request.get_json()
    if update_dict is None:
        return (jsonify({'error': 'Not a JSON'}), 400)

    id_city = storage.get('City', city_id)
    if id_city:
        ignore_key = ['id', 'created_at', 'updated_at', 'state_id']
        for key, value in update_dict.items():
            if key not in ignore_key:
                setattr(id_city, key, value)
        id_city.save()
        return (jsonify(id_city.to_dict()), 200)
    else:
        abort(404)
