#!/usr/bin/python3
"""HTTP methods for state  """

from api.v1.views import app_views
from models import storage
from flask import Flask, jsonify, abort, request
from models.state import State


@app_views.route('/states', strict_slashes=False,  methods=['GET'])
@app_views.route('/states/<state_id>', strict_slashes=False,  methods=['GET'])
def get_state(state_id=None):
    """Retrieves the list of all State objects or  retrieves a State object"""
    if state_id is None:
        list_state = []
        objects = storage.all('State')
        for obj in objects.values():
            list_state.append(obj.to_dict())
        return(jsonify(list_state))
    else:
        id_state = storage.get('State', state_id)
        if id_state:
            return (jsonify(id_state.to_dict()))
        else:
            abort(404)


@app_views.route('/states/<state_id>',
                 strict_slashes=False,
                 methods=['DELETE'])
def delete_state(state_id=None):
    """Deletes a State object"""
    id_state = storage.get('State', state_id)
    if id_state:
        storage.delete(id_state)
        storage.save()
        return (jsonify({}), 200)
    else:
        abort(404)

@app_views.route('/states', strict_slashes=False,  methods=['POST'])
def post_state():
    """ Creates a State """
    dict_request = request.get_json()
    if  dict_request is None:
        return (jsonify({'error': 'Not a JSON'}), 400)
    
    if 'name' not in dict_request:
         return (jsonify({'error': 'Missing name'}), 400)
         
    new_obj = State(**dict_request)
    new_obj.save()
    return (jsonify(new_obj.to_dict()), 201)
