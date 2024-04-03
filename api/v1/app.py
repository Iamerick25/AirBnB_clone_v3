#!/usr/bin/python3
"""Starts a threaded flask web application"""

from api.v1.views import app_views
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from os import environ, getenv

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix="/api/v1")
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.errorhandler(404)
def page_not_found(e):
    """handler for 404 errors that returns a JSON-formatted 404 response"""
    resp = jsonify({'error': 'Not found'})
    resp.status_code = 404
    return resp


@app.teardown_appcontext
def teardown_storage(x):
    """calls close() on storage"""
    storage.close()


if __name__ == '__main__':
    if 'HBNB_API_HOST' in environ:
        hbnb_api_host = getenv('HBNB_API_HOST')
    else:
        hbnb_api_host = '0.0.0.0'
    if 'HBNB_API_PORT' in environ:
        hbnb_api_port = getenv('HBNB_API_PORT')
    else:
        hbnb_api_port = 5000
    app.run(host=hbnb_api_host, port=hbnb_api_port, threaded=True)
