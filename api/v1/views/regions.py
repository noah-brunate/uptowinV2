#!/usr/bin/python3
"""State module"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.region import Region
from flasgger.utils import swag_from


@app_views.route('/regions', methods=['GET'], strict_slashes=False)
@swag_from('documentation/region/get.yml', methods=['GET'])
def get_all():
    """ get all regions """
    all_list = [obj.to_dict() for obj in storage.all(Region).values()]
    return jsonify(all_list)


@app_views.route('/regions/<string:region_id>', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/region/get_id.yml', methods=['GET'])
def get_method_region(region_id):
    """ get region by id"""
    reg = storage.get(Region, region_id)
    if reg is None:
        abort(404)
    return jsonify(reg.to_dict())


@app_views.route('/regions/<string:region_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/region/delete.yml', methods=['DELETE'])
def del_method(region_id):
    """ delete region by id"""
    reg = storage.get(Region, region_id)
    if reg is None:
        abort(404)
    reg.delete()
    storage.save()
    return jsonify({})


@app_views.route('/regions/', methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/region/post.yml', methods=['POST'])
def create_obj():
    """ create new instance """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    js = request.get_json()
    obj = Region(**js)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/regions/<string:region_id>', methods=['PUT'],
                 strict_slashes=False)
@swag_from('documentation/region/put.yml', methods=['PUT'])
def post_method(region_id):
    """ post method """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    obj = storage.get(Region, region_id)
    if obj is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated']:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict())
