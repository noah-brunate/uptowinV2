#!/usr/bin/python
""" holds class Local"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship

class Local(BaseModel, Base):
    """Representation of Local """
    if models.storage_t == 'db':
        __tablename__ = 'locals'
        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        title = Column(String(128), nullable=False)
        limit = Column(Integer, nullable=False)
        description = Column(String(1024), nullable=True)
        invite = Column(String(128), nullable=False)
        location = Column(String(128), nullable=False)
    else:
        city_id = ""
        user_id = ""
        title = ""
        limit = 0
        description = ""
        invite = ""
        location = ""

    def __init__(self, *args, **kwargs):
        """initializes Place"""
        super().__init__(*args, **kwargs)
