from flask import jsonify, request
from server.auth.models import User
from server.auth import auth_bp
from server.config import db

@auth_bp.route('/get_public_data/<int:user_id>', methods=['GET'])
def get_public_data(user_id):
    """
    Retrieve public data for a specific user by user_id.
    Returns the bio, interests, songs, and other profile fields.
    """
    # Query for the user by ID
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Create a dictionary with the public data
    public_data = {
        "bio": user.bio,
        "interests": user.interests,
        "songs": user.songs,
        "other": user.other
    }
    return jsonify(public_data), 200


@auth_bp.route('/get_all_user_data/<int:user_id>', methods=['GET'])
def get_all_user_data(user_id):
    """
    Retrieve all data for a specific user by user_id.
    """
    # Query for the user by ID
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Create a dictionary with all user data
    all_user_data = {
        "id": user.id,
        "name": user.name,
        "phone_number": user.phone_number,
        "bio": user.bio,
        "interests": user.interests,
        "songs": user.songs,
        "instagram": user.instagram,
        "snapchat": user.snapchat,
        "other": user.other,
    }
    
    return jsonify(all_user_data), 200