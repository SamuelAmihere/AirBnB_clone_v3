#!/usr/bin/python3
"""For a Flask web application api
"""
from api.v1.views import app_views
from flask_cors import CORS, cross_origin
from flask import Flask, jsonify, make_response, render_template
from werkzeug.exceptions import HTTPException
import os
from models import storage


app = Flask(__name__)

var_host = 'HBNB_API_HOST'
var_port = 'HBNB_API_PORT'
default_host = '0.0.0.0'
default_port = '5000'

host = os.getenv(var_host, default_host)
port = int(os.getenv(var_port, default_port))

# BluePrint of app_views defined in api/v1/views
app.register_blueprint(app_views)

# set global strict slashes
app.url_map.strict_slashes = False

# Ensuring cross-origin resource sharing among components
CORS(app, resources={'/*': {'origins': "*"}})


# page rendering
@app.errorhandler(404)
def handle_404(e):
    """andles 404 errors"""
    message = e.description if isinstance(e, Exception) and \
            hasattr(e, 'description') else 'Bad request'
    return jsonify(error=msg), 400


@app.errorhandler(404)
def error_404(error):
    """Handles 404 HTTP error code"""
    return jsonify(error='Not found'), 404


@app.teardown_appcontext
def teardown_flask(exception):
    """The app(request) context ends event listener
    by closing storage
    """
    # print(exception)
    storage.close()


if __name__ == "__main__":
    # start Flask app
    app.run(
        host=host,
        port=port,
        threaded=True
    )
