from flask import jsonify, request
from server.auth.models import User
from server.auth import auth_bp
from server.config import db
import firebase_admin
from firebase_admin import auth, credentials, initialize_app
from flask import request, jsonify
from server.auth.models import User
from server.config import db

cred = credentials.Certificate("firebase.json")
firebase_admin.initialize_app(cred)

def verify_firebase_token(id_token):
    try:
        # Verify the Firebase ID token
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']
        # Perform any additional checks or authentication steps here
        return uid  # or other information you want to use
    except auth.InvalidIdTokenError:
        return None
    
from server.auth import auth_bp

@auth_bp.route("/signup", methods=["POST"])
def signup():
        data = request.get_json()

        # Extract data from request
        id = data.get("id")
        name = data.get("name")
        phone_number = data.get("number")
        bio = data.get("bio")
        interests = data.get("interests", [])
        songs = data.get("songs", [])
        handshake_card = data.get("card", {"design": 0, "color": "#FFFFFF"})
        instagram = data.get("instagram")
        snapchat = data.get("snapchat")
        other = data.get("other")

        # Create a new User object
        new_user = User(
            id=id,
            name=name,
            phone_number=phone_number,
            bio=bio,
            interests=interests,
            songs=songs,
            handshake_card=handshake_card,
            instagram=instagram,
            snapchat=snapchat,
            other=other
        )

        # Add the new user to the session and commit
        db.session.add(new_user)
        db.session.commit()

@auth_bp.route('/get_public_data/<int:user_id>/<int:requester_id>', methods=['GET'])
def get_public_data(user_id, requester_id):
    """
    Retrieve public data for a specific user by user_id.
    Only returns the bio, handshake_card, songs, other profile fields,
    and intersecting interests with the requester.
    """
    # Query for both the specified user and the requester
    user = User.query.get(user_id)
    requester = User.query.get(requester_id)
    
    if not user or not requester:
        return jsonify({"error": "One or both users not found"}), 404

    # Calculate the intersecting interests if both have interests
    if user.interests and requester.interests:
        intersecting_interests = list(set(user.interests).intersection(set(requester.interests)))
    else:
        intersecting_interests = []

    # Construct the public data response
    public_data = {
        "bio": user.bio,
        "interests": intersecting_interests,
        "songs": user.songs,
        "other": user.other,
        "handshake_card": user.handshake_card
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
        "handshake_card": user.handshake_card,
        "interests": user.interests,
        "songs": user.songs,
        "instagram": user.instagram,
        "snapchat": user.snapchat,
        "other": user.other,
    }
    
    return jsonify(all_user_data), 200