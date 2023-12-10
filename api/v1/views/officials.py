#!/usr/bin/python3
"""
This file contains the Amenity module
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.official import Official
from flasgger.utils import swag_from


@app_views.route('/officials', methods=['GET'], strict_slashes=False)
@swag_from('documentation/official/get.yml', methods=['GET'])
def get_all_officials():
    """ get officials by id """
    all_list = [obj.to_dict() for obj in storage.all(Official).values()]
    return jsonify(all_list)


@app_views.route('/official/<string:official_id>', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/official/get_id.yml', methods=['GET'])
def get_official(official_id):
    """ get official by id"""
    off = storage.get(Official, official_id)
    if off is None:
        abort(404)
    return jsonify(off.to_dict())


@app_views.route('/officials/<string:official_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/official/delete.yml', methods=['DELETE'])
def del_official(official_id):
    """ delete official by id"""
    off = storage.get(Official, official_id)
    if off is None:
        abort(404)
    off.delete()
    storage.save()
    return jsonify({})


@app_views.route('/officials/', methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/official/post.yml', methods=['POST'])
def create_obj_official():
    """ create new instance """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    js = request.get_json()
    obj = Official(**js)
    obj.save()
    return (jsonify(obj.to_dict()), 201)


@app_views.route('/officials/<string:official_id>', methods=['PUT'],
                 strict_slashes=False)
@swag_from('documentation/official/put.yml', methods=['PUT'])
def post_official(official_id):
    """  """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    obj = storage.get(Official, official_id)
    if obj is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict())
