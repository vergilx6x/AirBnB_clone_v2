#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        if (cls is None):
            return FileStorage.__objects

        else:
            new_dict = {}
            for k, v in self.__objects.items():
                if isinstance(v, cls):
                    new_dict[k] = v
            return new_dict

    def new(self, obj):
        """Adds new object to storage dictionary"""
        self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, 'w') as f:
            temp = {}
            temp.update(FileStorage.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

    def delete(self, obj=None):
        """delete obj from __objects"""
        if obj is None:
            return

        key = obj.__class__.__name__ + "." + obj.id
        del self.__objects[key]
        self.save()

    def close(self):
        """ Calls reload """

        self.reload()

    def reload(self):
        """Loads storage dictionary from file"""

        classes = {
                    'BaseModel': BaseModel, 'User': User, 'Place': Place,
                    'State': State, 'City': City, 'Amenity': Amenity,
                    'Review': Review
                  }
        try:
            temp = {}
            with open(FileStorage.__file_path, 'r', encoding="UTF-8") as f:
                if not f.read().strip():
                    return
                f.seek(0)
                temp = json.load(f)
                for key, val in temp.items():
                    self.all()[key] = classes[val['__class__']](**val)
        except FileNotFoundError:
            pass
