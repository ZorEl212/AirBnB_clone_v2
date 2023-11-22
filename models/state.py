#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import Base, BaseModel
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship("City",  backref="state", cascade="delete")

    @property
    def cities(self):
        """Get a list of all related City objects."""
        city_list = []
        for city in list(storage.all(City).values()):
            if city.state_id == self.id:
                city_list.append(city)
        return city_list
