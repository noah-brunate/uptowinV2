#!/usr/bin/python3
"""
This file contains the Amenity module
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.intern import Intern
from flasgger.utils import swag_from


@app_views.route('/internships', methods=['GET'], strict_slashes=False)
@swag_from('documentation/internship/get.yml', methods=['GET'])
def get_all_internships():
    """ get internship by id """
    all_list = [obj.to_dict() for obj in storage.all(Intern).values()]
    return jsonify(all_list)


@app_views.route('/internships/<string:intern_id>', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/internship/get_id.yml', methods=['GET'])
def get_internship(intern_id):
    """ get internship by id"""
    inter = storage.get(Intern, intern_id)
    if inter is None:
        abort(404)
    return jsonify(inter.to_dict())


@app_views.route('/internships/<string:intern_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/internship/delete.yml', methods=['DELETE'])
def del_internship(intern_id):
    """ delete internship by id"""
    inter = storage.get(Intern, intern_id)
    if inter is None:
        abort(404)
    inter.delete()
    storage.save()
    return jsonify({})


@app_views.route('/internships/', methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/internship/post.yml', methods=['POST'])
def create_obj_internship():
    """ create new instance """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    js = request.get_json()
    obj = Intern(**js)
    obj.save()
    return (jsonify(obj.to_dict()), 201)


@app_views.route('/internships/<string:intern_id>', methods=['PUT'],
                 strict_slashes=False)
@swag_from('documentation/internship/put.yml', methods=['PUT'])
def post_internship(intern_id):
    """  """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    obj = storage.get(Intern, intern_id)
    if obj is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict())
