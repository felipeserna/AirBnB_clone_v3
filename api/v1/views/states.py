#!/usr/bin/python3
"""HTTP methods for state  """

from api.v1.views import app_views
from models import storage
from flask import Flask, jsonify, abort
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
