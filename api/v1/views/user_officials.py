#!/usr/bin/python3
"""user_officials.py"""
import os
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.official import Official
from models.user import User
from flasgger.utils import swag_from


@app_views.route('/users/<string:user_id>/officials', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/user_official/get_id.yml', methods=['GET'])
def get_officials(user_id):
    """ retrieves all oficials from a user """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    officials = [obj.to_dict() for obj in user.Officials]
    return jsonify(officials)


@app_views.route('/users/<string:user_id>/officials/<string:official_id>',
                 methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/user_official/delete.yml', methods=['DELETE'])
def delete_official(user_id, official_id):
    """ delete an official from a user """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    official = storage.get(Official, official_id)
    if official is None:
        abort(404)
    if official not in user.Officials:
        abort(404)
    user.Officials.remove(official)
    storage.save()
    return jsonify({})


@app_views.route('/users/<string:user_id>/user_official/<string:official_id>',
                 methods=['POST'], strict_slashes=False)
@swag_from('documentation/user_official/post.yml', methods=['POST'])
def post_official(user_id, official_id):
    """ post an official by id """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    official = storage.get(Official, official_id)
    if official is None:
        abort(404)
    if official in user.officials:
        return (jsonify(official.to_dict()), 200)
    user.Officials.append(official)
    storage.save()
    return (jsonify(official.to_dict(), 201))
