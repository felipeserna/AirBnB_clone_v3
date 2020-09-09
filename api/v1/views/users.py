#!/usr/bin/python3
"""HTTP methods for User  """

from api.v1.views import app_views
from models import storage
from flask import Flask, jsonify, abort, request
from models.user import User


@app_views.route('/users', strict_slashes=False,  methods=['GET'])
@app_views.route('/users/<user_id>', strict_slashes=False,  methods=['GET'])
def get_user(user_id=None):
    """Retrieves the list of all users objects or  retrieves a User object"""
    if user_id is None:
        list_users = []
        objects = storage.all('User')
        for obj in objects.values():
            list_users.append(obj.to_dict())
        return(jsonify(list_users))
    else:
        id_user = storage.get('User', user_id)
        if id_user:
            return (jsonify(id_user.to_dict()))
        else:
            abort(404)


@app_views.route('/users/<user_id>',
                 strict_slashes=False,
                 methods=['DELETE'])
def delete_user(user_id=None):
    """Deletes a user object"""
    id_user = storage.get('User', user_id)
    if id_user:
        storage.delete(id_user)
        storage.save()
        return (jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/users',
                 strict_slashes=False,  methods=['POST'])
def post_user():
    """ Creates a User """

    dict_request = request.get_json()
    if dict_request is None:
        return (jsonify({'error': 'Not a JSON'}), 400)

    if 'email' not in dict_request:
        return (jsonify({'error': 'Missing email'}), 400)
    if 'password' not in dict_request:
        return (jsonify({'error': 'Missing password'}), 400)

    new_obj = User(**dict_request)
    new_obj.save()
    return (jsonify(new_obj.to_dict()), 201)


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['PUT'])
def put_user(user_id=None):
    """ Updates a User """
    update_dict = request.get_json()
    if update_dict is None:
        return (jsonify({'error': 'Not a JSON'}), 400)

    id_user = storage.get('User', user_id)
    if id_user:
        ignore_key = ['id', 'created_at', 'updated_at', 'email']
        for key, value in update_dict.items():
            if key not in ignore_key:
                setattr(id_user, key, value)
        id_user.save()
        return (jsonify(id_user.to_dict()), 200)
    else:
        abort(404)
