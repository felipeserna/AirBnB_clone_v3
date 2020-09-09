#!/usr/bin/python3
"""
Creates an instance of Blueprint
"""

from api.v1.views import app_views
from models import storage
from flask import Flask, jsonify


@app_views.route('/status', methods=['GET'])
def status():
    """returns the status in JSON"""
    return (jsonify({'status': 'OK'}))


@app_views.route('/stats')
def stats():
    """  retrieves the number of each objects by type """
    dic_stats = {
        "amenities": storage.count('Amenity'),
        "cities": storage.count('City'),
        "places": storage.count('Place'),
        "reviews": storage.count('Review'),
        "states": storage.count('State'),
        "users": storage.count('User')
    }
    return (jsonify(dic_stats))
