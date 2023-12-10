#!/usr/bin/python
""" holds class Region"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship

class Region(BaseModel, Base):
    """Representation of Region """
    if models.storage_t == "db":
        __tablename__ = 'regions'
        name = Column(String(128), nullable=False)
        states = relationship("State", backref="region")
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """initializes city"""
        super().__init__(*args, **kwargs)
