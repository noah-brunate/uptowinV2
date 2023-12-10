#!/usr/bin/python3
"""places_amenities.py"""
import os
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.local import Local
from models.user import User
from flasgger.utils import swag_from


@app_views.route('/users/<string:user_id>/locals', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/user_local/get_id.yml', methods=['GET'])
def get_locals(user_id):
    """ retrieves all locals from a user """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    locs = [obj.to_dict() for obj in user.Locals]
    return jsonify(locs)


@app_views.route('/users/<string:user_id>/locals/<string:local_id>',
                 methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/user_local/delete.yml', methods=['DELETE'])
def delete_amenity(user_id, local_id):
    """ delete local from user """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    loc = storage.get(Local, local_id)
    if loc is None:
        abort(404)
    if loc not in user.Locals:
        abort(404)
    user.Locals.remove(loc)
    storage.save()
    return jsonify({})


@app_views.route('/users/<string:user_id>/locals/<string:local_id>',
                 methods=['POST'], strict_slashes=False)
@swag_from('documentation/user_local/post.yml', methods=['POST'])
def post_local(user_id, local_id):
    """ post local by id """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    local = storage.get(Local, local_id)
    if local is None:
        abort(404)
    if local in user.Locals:
        return (jsonify(local.to_dict()), 200)
    user.Locals.append(local)
    storage.save()
    return (jsonify(local.to_dict(), 201))
