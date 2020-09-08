#!/usr/bin/python3
"""
Creates an instance of Blueprint
"""

from api.v1.views import app_views
from flask import Flask, jsonify


@app_views.route('/status', methods=['GET'])
def status():
    """returns the status in JSON"""
    return (jsonify({'status': 'OK'}))
