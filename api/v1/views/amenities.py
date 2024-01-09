#!/usr/bin/python3
"""Renders amenities info"""
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from flask import jsonify, request
from werkzeug.exceptions import NotFound, MethodNotAllowed, BadRequest
from .commons import (manipulate, fetch_data, fetch_data_id, fetch_process,
                      reach_endpoint, allows, err_msg)


def get_amenities(amenity_id=None):
    """Returns the amenities sing the given id.
    """
    am_all = fetch_data(Amenity)
    if amenity_id:
        results = manipulate(filter, amenity_id, am_all)
        if results:
            return jsonify(results[0].to_dict())
        raise NotFound()
    am_all = manipulate(map, None, am_all)
    return jsonify(am_all)


def add_amenity(amenity_id=None):
    """Add new amenity into the system.
    """
    req_d = request.get_json()
    if type(req_d) is not dict:
        raise BadRequest(description='Not a JSON')
    if 'name' not in req_d:
        raise BadRequest(description='Missing name')
    am_obj = Amenity(**req_d)
    am_obj.save()
    return jsonify(am_obj.to_dict()), 201


def delete_amenity(amenity_id=None):
    """Deletes amenity using given id.
    """
    results = fetch_process(Amenity, filter, amenity_id)
    if results:
        storage.delete(results[0])
        storage.save()
        return jsonify({}), 200
    raise NotFound()


def update_amenity(amenity_id=None):
    """"Updates amenity given id.
    """
    table_cols = ('id', 'created_at', 'updated_at')

    results = fetch_process(Amenity, filter, amenity_id)

    if results:
        data = request.get_json()
        if type(data) is not dict:
            raise BadRequest(description='Not a JSON')
        am_old = results[0]
        for key, value in data.items():
            if key not in table_cols:
                setattr(am_old, key, value)
        am_old.save()
        return jsonify(am_old.to_dict()), 200
    raise NotFound()


@app_views.route('/amenities', methods=allows)
@app_views.route('/amenities/<amenity_id>', methods=allows)
def handle_amenities(amenity_id=None):
    """Handles amenities endpoint.
    """
    am_handlers = reach_endpoint([get_amenities, add_amenity, delete_amenity, update_amenity])

    rm = request.method
    if rm in am_handlers:
        return am_handlers[rm](amenity_id)
    else:
        raise MethodNotAllowed(allows)
