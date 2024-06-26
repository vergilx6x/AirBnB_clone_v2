#!/usr/bin/python3
""" State Module for HBNB project """
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String
import models
import shlex


class State(BaseModel, Base):
    """This is the class for State
    Attributes:
        name.
    """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship("City", cascade='all, delete, delete-orphan',
                          backref="state")

    @property
    def cities(self):
        models = models.storage.all()
        list_cities = []
        result = []
        for key in models:
            city = key.replace('.', ' ')
            city = shlex.split(city)
            if (city[0] == 'City'):
                list_cities.append(models[key])
        for obj in list_cities:
            if (obj.state_id == self.id):
                result.append(obj)
        return (result)
