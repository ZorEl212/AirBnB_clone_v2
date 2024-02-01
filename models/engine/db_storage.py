#!/usr/bin/python3
"""This module defines a class to manage Database storage"""
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from models.base_model import BaseModel, Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class DBStorage:
    """This class manages storage of hbnb models in structured format"""

    __engine = None
    __session = None

    def __init__(self):
        """creates the engine"""
        self.__engine = create_engine(
            "mysql+mysqldb://{}:{}@{}/{}".format(getenv("HBNB_MYSQL_USER"),
                                                 getenv("HBNB_MYSQL_PWD"),
                                                 getenv("HBNB_MYSQL_HOST"),
                                                 getenv("HBNB_MYSQL_DB")),
            pool_pre_ping=True)

        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query the table on the current database session"""
        objs = []

        if cls is None:
            classes_to_query = [State, City, User, Place, Review, Amenity]
            for class_to_query in classes_to_query:
                objs.extend(self.__session.query(class_to_query).all())
        else:
            objs = self.__session.query(cls).all()

        # Exclude '_sa_instance_state' from the dictionaries
        result = {
            "{}.{}".format(type(o).__name__, o.id): {
                key: value for key, value in o.__dict__.items()
                       if key != '_sa_instance_state'  # noqa: E131
            } for o in objs
        }

        return result

    def new(self, obj):
        '''adds the obj to the current db session'''
        if obj is not None:
            try:
                self.__session.add(obj)
                self.__session.flush()
                self.__session.refresh(obj)
            except Exception as ex:
                self.__session.rollback()
                raise ex

    def save(self, obj=None):
        """Commit all changes of the current database session."""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete obj from the current database session."""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database and initialize a new session."""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        self.__session.close()
