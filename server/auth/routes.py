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



