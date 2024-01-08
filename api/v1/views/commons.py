#!/usr/bin/bash
"""Has functions and other items common to all views"""
from models import storage


# helpers
def manipulate(fn, id_, data):
    """A helper func that applies a given function on data using id_"""
    if fn is filter:
        return list(filter(lambda x: x.id == id_, data))
    elif fn is map:
        return list(map(lambda x: x.to_dict(), data))


def fetch_data(obj):
    """Retrieves data from data base"""
    return storage.all(obj).values()


def fetch_process(obj, fn, id_):
    """Retrieve and process data"""
    data = fetch_data(obj)
    return manipulate(fn, id_, data)
