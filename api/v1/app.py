#!/usr/bin/python3
"""
starts a Flask web application
"""

from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage
from os import getenv


# create an instance of the Flask class
app = Flask(__name__)
app.url_map.strict_slashes = False

host = getenv('HBNB_API_HOST')
port = getenv('HBNB_API_PORT')

if not host:
    host = "0.0.0.0"

if not port:
    port = 5000

app.register_blueprint(app_views)


@app.teardown_appcontext
def remove_session(self):
    """after each request removes the current SQLAlchemy Session"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """handler for 404 errors that returns a status code response"""
    return (jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    app.run(host=host, port=port, threaded=True)
