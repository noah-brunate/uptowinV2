#!/usr/bin/python3
"""places_amenities.py"""
import os
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.intern import Intern
from models.user import User
from flasgger.utils import swag_from


@app_views.route('/users/<string:user_id>/internships', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/user_intern/get_id.yml', methods=['GET'])
def get_internships(user_id):
    """ retrieves all internships from a user """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    internships = [obj.to_dict() for obj in user.Internships]
    return jsonify(internships)


@app_views.route('/users/<string:user_id>/internships/<string:internship_id>',
                 methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/user_internships/delete.yml', methods=['DELETE'])
def delete_internship(user_id, internship_id):
    """ delete internship from user """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    internship = storage.get(Intern, internship_id)
    if internship is None:
        abort(404)
    if internship not in user.Internships:
        abort(404)
    user.Internships.remove(internship)
    storage.save()
    return jsonify({})


@app_views.route('/users/<string:user_id>/internships/<string:internship_id>',
                 methods=['POST'], strict_slashes=False)
@swag_from('documentation/user_internship/post.yml', methods=['POST'])
def post_internship(user_id, internship_id):
    """ post internship by id """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    internship = storage.get(Intern, internship_id)
    if internship is None:
        abort(404)
    if internship in user.Internships:
        return (jsonify(internship.to_dict()), 200)
    user.Internships.append(internship)
    storage.save()
    return (jsonify(internship.to_dict(), 201))
