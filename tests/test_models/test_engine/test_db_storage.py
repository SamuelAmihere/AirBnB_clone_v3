#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8
import unittest
DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


@unittest.skipIf(models.storage_t != 'db', "not testing db storage")
class TestDBStorage(unittest.TestCase):
    """Test the FileStorage class"""
    def setUp(self):
        """initializes new user for testing"""
        self.s = State(name='Alabama')

        self.s.save()

    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""

    def test_new(self):
        """test that new adds an object to the database"""

    def test_save(self):
        """Test that save properly saves objects to file.json"""

    def test_get(self):
        """testing for get on object of a returned class by id"""
        storage = models.storage

        self.assertIsNone(storage.get(int, self.s.id))
        self.assertIsNone(storage.get(State, self.s.id + 'op'))
        self.assertEqual(self.s.id, storage.get(State, self.s.id).id)
        self.assertEqual(self.s.name, storage.get(State, self.s.id).name)
        self.assertIsNot(self.s, storage.get(State, self.s.id + 'op'))
        self.assertIsNone(storage.get(State, 45))
        self.assertIsNone(storage.get(None, self.s.id))

        with self.assertRaises(TypeError):
            storage.get()
        with self.assertRaises(TypeError):
            storage.get(State, self.s.id, 'op')
        with self.assertRaises(TypeError):
            storage.get(State)

    def test_count(self):
        """test that count returns the number of objects of a given class."""
        storage = models.storage
        self.assertIs(type(storage.count(State)), int)
        self.assertIs(type(storage.count(None)), int)
        self.assertIs(type(storage.count()), int)
        self.assertEqual(storage.count(), storage.count(None))
        self.assertIs(type(storage.count(int)), int)
        self.assertEqual(storage.count(), storage.count(None))
        State(name='Lagos').save()
        self.assertGreater(storage.count(State), 0)
        cn = storage.count(State)
        State(name='Kasablanca').save()
        self.assertGreater(storage.count(State), cn)
        Amenity(name='Fast WiFi').save()
        Amenity(name='Free AC').save()
        self.assertGreater(storage.count(), storage.count(State))

        with self.assertRaises(TypeError):
            storage.count(State, 'op')

    def test_all_reload_save(self):
        """... checks if all(), save(), and reload function
        in new instance.  This also tests for reload"""
        actual = 0
        db_objs = storage.all()
        for obj in db_objs.values():
            for x in [self.s.id]:
                if x == obj.id:
                    actual += 1
        self.assertGreater(actual, 0)
