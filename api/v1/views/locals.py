#!/usr/bin/python3
"""
This file contains the Amenity module
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.local import Local
from flasgger.utils import swag_from


@app_views.route('/Locals', methods=['GET'], strict_slashes=False)
@swag_from('documentation/local/get.yml', methods=['GET'])
def get_all_locals():
    """ get locals by id """
    all_list = [obj.to_dict() for obj in storage.all(Local).values()]
    return jsonify(all_list)


@app_views.route('/Locals/<string:local_id>', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/local/get_id.yml', methods=['GET'])
def get_local(local_id):
    """ get local by id"""
    local = storage.get(Local, local_id)
    if local is None:
        abort(404)
    return jsonify(local.to_dict())


@app_views.route('/Locals/<string:local_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/local/delete.yml', methods=['DELETE'])
def del_local(local_id):
    """ delete local by id"""
    local = storage.get(Local, local_id)
    if local is None:
        abort(404)
    local.delete()
    storage.save()
    return jsonify({})


@app_views.route('/Locals/', methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/local/post.yml', methods=['POST'])
def create_obj_local():
    """ create new instance """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    js = request.get_json()
    obj = Local(**js)
    obj.save()
    return (jsonify(obj.to_dict()), 201)


@app_views.route('/locals/<string:local_id>', methods=['PUT'],
                 strict_slashes=False)
@swag_from('documentation/local/put.yml', methods=['PUT'])
def post_local(local_id):
    """ """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    obj = storage.get(Local, local_id)
    if obj is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict())
