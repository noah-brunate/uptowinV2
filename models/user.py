#!/usr/bin/python3
""" holds class User"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, Table, ForeignKey
from sqlalchemy.orm import relationship


if models.storage_t == 'db':
    User_intern = Table('User_intern', Base.metadata,
                          Column('user_id', String(60),
                                 ForeignKey('users.id', onupdate='CASCADE',
                                            ondelete='CASCADE'),
                                 primary_key=True),
                          Column('internship_id', String(60),
                                 ForeignKey('internships.id', onupdate='CASCADE',
                                            ondelete='CASCADE'),
                                 primary_key=True))
    
    User_local = Table('User_local', Base.metadata,
                          Column('user_id', String(60),
                                 ForeignKey('users.id', onupdate='CASCADE',
                                            ondelete='CASCADE'),
                                 primary_key=True),
                          Column('local_id', String(60),
                                 ForeignKey('locals.id', onupdate='CASCADE',
                                            ondelete='CASCADE'),
                                 primary_key=True))
    
    User_official = Table('User_official', Base.metadata,
                          Column('user_id', String(60),
                                 ForeignKey('users.id', onupdate='CASCADE',
                                            ondelete='CASCADE'),
                                 primary_key=True),
                          Column('official_id', String(60),
                                 ForeignKey('officials.id', onupdate='CASCADE',
                                            ondelete='CASCADE'),
                                 primary_key=True))


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        phone = Column(String(128), nullable=False)
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        name = Column(String(128), nullable=True)
        status = Column(String(128))
        national_id = Column(String(128))

        Internships = relationship("Intern", secondary="User_intern",
                                 backref="Intern_user",
                                 viewonly=False)
        Officials = relationship("Official", secondary="User_official",
                                 backref="Official_user",
                                 viewonly=False)
        Locals = relationship("Local", secondary="User_local",
                                 backref="local_user",
                                 viewonly=False)
        Reviews = relationship("Review", backref="user")
    else:
        phone = ""
        email = ""
        password = ""
        name = ""
        status = ""
        national_id = ""
        skills = []

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)

    if models.storage_t != 'db':
        @property
        def Reviews(self):
            """getter attribute returns the list of Review instances"""
            from models.review import Review
            review_list = []
            all_reviews = models.storage.all(Review)
            for review in all_reviews.values():
                if review.place_id == self.id:
                    review_list.append(review)
            return review_list

        @property
        def Internships(self):
            """getter attribute returns the list of Amenity instances"""
            from models.intern import Intern
            intern_list = []
            all_internships = models.storage.all(Intern)
            for inter in all_internships.values():
                if inter.user_id == self.id:
                    intern_list.append(inter)
            return intern_list
        
        @property
        def Locals(self):
            """getter attribute returns the list of Review instances"""
            from models.local import Local
            local_list = []
            all_locals = models.storage.all(Local)
            for loc in all_locals.values():
                if loc.user_id == self.id:
                    local_list.append(loc)
            return local_list

        @property
        def Officials(self):
            """getter attribute returns the list of Amenity instances"""
            from models.official import Official
            official_list = []
            all_officials = models.storage.all(Official)
            for off in all_officials.values():
                if off.user_id == self.id:
                    official_list.append(off)
            return official_list
