#!/usr/bin/python3
"""HTTP methods for Place  """

from api.v1.views import app_views
from models import storage
from flask import Flask, jsonify, abort, request
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False,  methods=['GET'])
def places_from_city(city_id=None):
    """  list of all Place objects of a City """
    id_city = storage.get('City', city_id)
    if id_city:
        list_places = []
        for place in id_city.places:
            list_places.append(place.to_dict())
        return (jsonify(list_places))
    else:
        abort(404)


@app_views.route('/places/<place_id>', strict_slashes=False,  methods=['GET'])
def get_place(place_id=None):
    """ Retrieves a Place object """
    id_place = storage.get('Place', place_id)
    if id_place:
        return (jsonify(id_place.to_dict()))
    else:
        abort(404)


@app_views.route('/places/<place_id>',
                 strict_slashes=False,
                 methods=['DELETE'])
def delete_place(place_id=None):
    """Deletes a place object"""
    id_place = storage.get('Place', place_id)
    if id_place:
        storage.delete(id_place)
        storage.save()
        return (jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False,  methods=['POST'])
def post_place(city_id=None):
    """ Creates a Place """
    id_city = storage.get('City', city_id)
    if id_city is None:
        abort(404)

    dict_request = request.get_json()
    if dict_request is None:
        return (jsonify({'error': 'Not a JSON'}), 400)

    if 'name' not in dict_request:
        return (jsonify({'error': 'Missing name'}), 400)

    if 'user_id' not in dict_request:
        return (jsonify({'error': 'Missing user_id'}), 400)

    id_user = None

    id_user = storage.get('User', dict_request['user_id'])
    if id_user is None:
        abort(404)

    dict_request['city_id'] = city_id

    new_obj = Place(**dict_request)
    new_obj.save()
    return (jsonify(new_obj.to_dict()), 201)


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['PUT'])
def put_place(place_id=None):
    """ Updates a place """
    update_dict = request.get_json()
    if update_dict is None:
        return (jsonify({'error': 'Not a JSON'}), 400)

    id_place = storage.get('Place', place_id)
    if id_place:
        ignore_key = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
        for key, value in update_dict.items():
            if key not in ignore_key:
                setattr(id_place, key, value)
        id_place.save()
        return (jsonify(id_place.to_dict()), 200)
    else:
        abort(404)
