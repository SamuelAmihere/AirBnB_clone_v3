#!/usr/bin/python3
'''API Views: Cities'''

from api.v1.views import app_views
from models import storage_t, storage
from models.city import City
from models.state import State
from models.place import Place
from models.review import Review
from flask import jsonify, request
from werkzeug.exceptions import NotFound, MethodNotAllowed, BadRequest
from .commons import (manipulate, fetch_data, fetch_data_id, fetch_process,
                      reach_endpoint, allows, err_msg)


def get_cities(state_id=None, city_id=None):
    """Returns the citiy from state using the given ids.
    """
    if state_id:
        st = fetch_data_id(State, state_id)
        if st:
            cities = manipulate(map, None, st.cities)
            return jsonify(cities)
    elif city_id:
        city = fetch_data_id(City, city_id)
        if city:
            return jsonify(city.to_dict())
    raise NotFound()


def add_city(state_id=None, city_id=None):
    '''Adds a new city.
    '''
    state = fetch_data_id(State, state_id)

    if not state:
        raise NotFound()
    data = request.get_json()
    if type(data) is not dict:
        raise BadRequest(description=err_msg[0])
    if 'name' not in data:
        raise BadRequest(description=err_msg[1])
    data['state_id'] = state_id
    city = City(**data)
    city.save()
    return jsonify(city.to_dict()), 201


def remove_city(state_id=None, city_id=None):
    """Deletes a state using given id.
    """
    if city_id:
        c = fetch_data_id(City, city_id)

        if c:
            storage.delete(c)
            if storage_t != "db":
                for place in fetch_data(Place):
                    if place.city_id == city_id:
                        for review in fetch_data(Review):
                            if review.place_id == place.id:
                                storage.delete(review)
                        storage.delete(place)
            storage.save()

            return jsonify({}), 200
    raise NotFound()


def update_city(state_id=None, city_id=None):
    """"Updates city db using state and its id.
    """
    cols = ('id', 'state_id', 'created_at', 'updated_at')

    if city_id:
        city = fetch_data_id(City, city_id)
        if city:
            data = request.get_json()
            if type(data) is not dict:
                raise BadRequest(description=err_msg[0])
            for key, value in data.items():
                if key not in cols:
                    setattr(city, key, value)
            city.save()
            return jsonify(city.to_dict()), 200
    raise NotFound()


@app_views.route('/states/<state_id>/cities', methods=allows[:2])
@app_views.route('/cities/<city_id>', methods=[allows[0], *allows[-2:]])
def handle_cities(state_id=None, city_id=None):
    '''Handles cities endpoint.
    '''
    handlers = reach_endpoint([get_cities, add_city, remove_city, update_city])

    if request.method in handlers:
        return handlers[request.method](state_id, city_id)
    else:
        raise MethodNotAllowed(list(handlers.keys()))
