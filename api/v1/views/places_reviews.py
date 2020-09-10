#!/usr/bin/python3
"""HTTP methods for Review  """

from api.v1.views import app_views
from models import storage
from flask import Flask, jsonify, abort, request
from models.review import Review
from models.user import User
from models.place import Place


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False,  methods=['GET'])
def review_from_place(place_id=None):
    """  list of all Review objects of a Place """
    id_place = storage.get('Place', place_id)
    if id_place:
        list_review = []
        for review in id_place.reviews:
            list_review.append(review.to_dict())
        return (jsonify(list_review))
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['GET'])
def get_review(review_id=None):
    """ Retrieves a Review object """
    id_review = storage.get('Review', review_id)
    if id_review:
        return (jsonify(id_review.to_dict()))
    else:
        abort(404)


@app_views.route('/reviews/<review_id>',
                 strict_slashes=False,
                 methods=['DELETE'])
def delete_review(review_id=None):
    """Deletes a review object"""
    id_review = storage.get('Review', review_id)
    if id_review:
        storage.delete(id_review)
        storage.save()
        return (jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False,  methods=['POST'])
def post_review(place_id=None):
    """ Creates a review """
    id_place = storage.get('Place', place_id)
    if id_place is None:
        abort(404)

    dict_request = request.get_json()
    if dict_request is None:
        return (jsonify({'error': 'Not a JSON'}), 400)

    if 'user_id' not in dict_request:
        return (jsonify({'error': 'Missing user_id'}), 400)

    id_user = None
    id_user = storage.get('User', dict_request['user_id'])
    if id_user is None:
        abort(404)

    if 'text' not in dict_request:
        return (jsonify({'error': 'Missing text'}), 400)

    dict_request['place_id'] = place_id

    new_obj = Review(**dict_request)
    new_obj.save()
    return (jsonify(new_obj.to_dict()), 201)


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['PUT'])
def put_review(review_id=None):
    """ Updates a review """
    update_dict = request.get_json()
    if update_dict is None:
        return (jsonify({'error': 'Not a JSON'}), 400)

    id_review = storage.get('Review', review_id)
    if id_review:
        ignore_key = ['id', 'created_at', 'updated_at', 'user_id', 'place_id']
        for key, value in update_dict.items():
            if key not in ignore_key:
                setattr(id_review, key, value)
        id_review.save()
        return (jsonify(id_review.to_dict()), 200)
    else:
        abort(404)
