#!/usr/bin/python3
"""Init file for views module"""
from flask import Blueprint


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')


from api.v1.views.index import *
from api.v1.views.locals import *
from api.v1.views.cities import *
from api.v1.views.officials import *
from api.v1.views.internships import *
from api.v1.views.users import *
from api.v1.views.user_locals import *
from api.v1.views.user_reviews import *
from api.v1.views.user_officials import *
from api.v1.views.user_internships import *

