#!/usr/bin/python3
'''API Views: Users'''
from models import storage
from models.user import User
from api.v1.views import app_views
from flask import jsonify, request
from werkzeug.exceptions import NotFound, BadRequest
from .commons import (fetch_data, fetch_data_id, delete_obj,
                      reach_endpoint, allows, clean_field)


info = ['email', 'password', 'first_name', 'last_name']
columns = ('id', info[0], 'created_at', 'updated_at')
err = ['Not a JSON', 'Missing email', 'Missing password']
choices = ['places', 'reviews']


def add_user(user_id=None):
    """ Adds a new user to the db."""
    
    post = {}    
    try:
        post = request.get_json()
    except Exception:
        post = None

    info_err = [(type(post), err[0]), (info[0], err[1]),
               (info[1], err[2])]
  
    if info_err[0][0] is not dict:
        raise BadRequest(description=info_err[0][1])
    if info_err[1][0] not in post:
        raise BadRequest(description=info_err[1][1])
    if info_err[2][0] not in post:
        raise BadRequest(description=info_err[2][1])
    user = User(**post)
    user.save()
    obj = clean_field(choices, user)
    return jsonify(obj), 201


def remove_user(user_id):
    '''Removes a user with the given id.
    '''
    user = fetch_data_id(User, user_id)
    if user:
        delete_obj(user)
        return jsonify({}), 200
    raise NotFound()


def update_user(user_id):
    '''Updates the user with the given id.
    '''
    user = fetch_data_id(User, user_id)
    if user:
        data = {}
        try:
            data = request.get_json()
        except Exception:
            data = None
        if type(data) is not dict:
            raise BadRequest(description=err[0])
        for key, value in data.items():
            if key not in columns:
                setattr(user, key, value)
        user.save()
        obj = clean_field(choices, user)
        return jsonify(obj), 200
    raise NotFound()

def get_users(user_id=None):
    '''Gets the user with the given id or all users.
    '''
    if user_id:
        user = fetch_data_id(User, user_id)
        if user:
            obj = clean_field(choices, user)
            return jsonify(obj)
        raise NotFound()
    all_users = fetch_data(User)
    users = [clean_field(choices, user) for user in all_users]
    return jsonify(users) 

@app_views.route('/users', methods=allows)
@app_views.route('/users/<user_id>', methods=allows)
def users_handler(user_id=None):
    '''Handles users endpoints.
    '''
    rm = request.method

    methods_endpt = reach_endpoint([get_users, add_user,
                                   remove_user, update_user])
    if rm in allows:
        return methods_endpt[rm](user_id)
    else:
        raise MethodNotAllowed(allows)
