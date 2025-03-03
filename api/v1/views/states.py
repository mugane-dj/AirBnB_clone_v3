#!/usr/bin/python3
"""
Module contains all endpoints to GET, POST, PUT OR DELETE
objects from State model.
"""


from models import storage
from models.state import State
from flask import jsonify
from api.v1.views import app_views
from flask import abort
from flask import request


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def get_all_states():
    """
    Retrieves the list of all State objects.
    """
    objs = storage.all(State).values()
    states = [obj.to_dict() for obj in objs]
    return jsonify(states)


@app_views.route("/states/<state_id>", methods=["GET"],
                 strict_slashes=False)
def get_state_by_id(state_id):
    """
    Retrieves a State object by id.
    """
    obj = storage.get(State, state_id)
    if obj:
        return jsonify(obj.to_dict())
    else:
        abort(404)


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_state_by_id(state_id):
    """
    Deletes a State object by id.
    """
    state = storage.get(State, state_id)
    if state:
        state.delete()
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state_obj():
    """
    Creates a new State object.
    """
    body = request.get_json()
    if body is None:
        return jsonify({"error": "Not a JSON"}), 400

    if "name" not in body.keys():
        return jsonify({"error": "Missing name"}), 400

    state = State(**body)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["PUT"],
                 strict_slashes=False)
def update_state_obj(state_id):
    """
    Updates a State object.
    """
    body = request.get_json()
    if body is None:
        return jsonify({"error": "Not a JSON"}), 400

    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in body.items():
        if key not in ignore_keys:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
