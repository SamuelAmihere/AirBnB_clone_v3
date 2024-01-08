#!/usr/bin/python3
'''API Views: States'''
from flask import request, jsonify
from werkzeug.exceptions import NotFound, MethodNotAllowed, BadRequest
from api.v1.views import app_views
from models.state import State
from models import storage
from .commons import manipulate, fetch_data, fetch_process


allows = ['GET', 'POST', 'DELETE', 'PUT']


# Endpoints
def get_states(state_id=None):
    """Returns the state using the given id/all if id not provided.
    """
    all_st = fetch_data(State)
    if state_id:
        results = manipulate(filter, state_id, all_st)
        if results:
            return jsonify(results[0].to_dict())
        raise NotFound()
    return jsonify(manipulate(map, state_id, all_st))


def remove_state(state_id=None):
    """Deletes a state using given id.
    """
    results = fetch_process(State, filter, state_id)
    if results:
        storage.delete(results[0])
        storage.save()
        return jsonify({}), 200
    raise NotFound()


def update_state(state_id=None):
    """"Updates state db using given id.
    """
    cols = ('id', 'created_at', 'updated_at')
    results = fetch_process(State, filter, state_id)
    if results:
        post = request.get_json()
        if type(post) is not dict:
            raise BadRequest(description='Not a JSON')
        prev = results[0]
        for key, value in post.items():
            if key not in cols:
                setattr(prev, key, value)
        prev.save()
        return jsonify(prev.to_dict()), 200
    raise NotFound()


def add_state(state_id=None):
    """Posting a new state.
    """
    msg = ['Not a JSON', 'Missing name']
    post = request.get_json()
    if type(post) is not dict:
        raise BadRequest(description=msg[0])
    if 'name' not in post:
        raise BadRequest(description=msg[1])
    new_st = State(**post)
    new_st.save()
    return jsonify(new_st.to_dict()), 201


@app_views.route('/states', methods=allows)
@app_views.route('/states/<state_id>', methods=allows)
def states_handler(state_id=None):
    '''Handles states endpoint.
    '''
    rm = request.method

    methods_endpt = {allows[n]: i for n, i in enumerate([get_states,
                                                        add_state,
                                                        remove_state,
                                                        update_state])}
    if rm in allows:
        return methods_endpt[rm](state_id)
    else:
        raise MethodNotAllowed(allows)
