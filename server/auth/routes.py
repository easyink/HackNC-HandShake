from flask import jsonify, request
from server.auth.models import User
from server.auth import auth_bp
from server.config import db
import firebase_admin
from firebase_admin import auth, credentials, initialize_app
import os

# cred = credentials.Certificate("C:\\Users\\adsle\\Source\\Repos\\HackNC-HandShake\\server\\auth\\handshake-nc-firebase-adminsdk-atc6h-30d3ad6f7d.json")
# cred = credentials.Certificate("C:\\Users\\adsle\\Source\\Repos\\HackNC-HandShake\\server\\auth\\handshake-nc-firebase-adminsdk-atc6h-30d3ad6f7d.json")
current_directory = os.path.dirname(os.path.abspath(__file__))
firebase_path = os.path.join(current_directory, 'firebase.json')

cred = credentials.Certificate(firebase_path)
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
        token = request.headers.get("Authorization")
        id = verify_firebase_token(token)
        if id:
            name = data.get("name")
            phone_number = data.get("phoneNumber")
            bio = data.get("bio")
            interests = data.get("interests", [])
            songs = data.get("songs", [])
            handshake_card = data.get("handshakeCard", {"design": 0, "color": "#FFFFFF"})
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

            return jsonify({"message": "User created successfully", "user_id": new_user.id}), 201
        return jsonify({"message": "User does not exist", "user_id": new_user.id}), 400

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
        "name": user.name,
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
    Retrieve all data for a specific user by user_id, if the requesting user has an incoming connection with this user.
    """
    requesting_user_id = request.json.get("requesting_user_id")
    if not requesting_user_id:
        return jsonify({"error": "Requesting user ID is required"}), 400

    # Query for the user by ID
    user = User.query.get(user_id)
    requesting_user = User.query.get(requesting_user_id)

    if not user or not requesting_user:
        return jsonify({"error": "One or both users not found"}), 404

    # Check if the requesting user has an incoming connection from the target user
    if not requesting_user.incoming_connections.filter_by(id=user.id).first():
        return jsonify({"error": "Access denied: No incoming connection from this user"}), 403

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


@auth_bp.route('/sort_connections_by_interests/<int:user_id>', methods=['GET'])
def sort_connections_by_interests(user_id):
    """
    Sort a user's connections based on the number of mutual interests, from most to least.
    """
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    connections = user.outgoing_connections.all()  # Get all connections
    connections_with_interest_count = []

    # Calculate mutual interests for each connection
    for connection in connections:
        mutual_interests = set(user.interests).intersection(set(connection.interests))
        connections_with_interest_count.append({
            "id": connection.id,
            "name": connection.name,
            "mutual_interest_count": len(mutual_interests),
            "mutual_interests": list(mutual_interests)
        })

    # Sort connections by the number of mutual interests (descending)
    sorted_connections = sorted(connections_with_interest_count, key=lambda x: x['mutual_interest_count'], reverse=True)

    return jsonify(sorted_connections), 200


@auth_bp.route('/sort_connections_by_songs/<int:user_id>', methods=['GET'])
def sort_connections_by_songs(user_id):
    """
    Sort a user's connections based on the number of mutually liked songs, from most to least.
    """
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    connections = user.outgoing_connections.all()  # Get all connections
    connections_with_song_count = []

    # Calculate mutual songs for each connection
    for connection in connections:
        mutual_songs = set(user.songs).intersection(set(connection.songs))
        connections_with_song_count.append({
            "id": connection.id,
            "name": connection.name,
            "mutual_song_count": len(mutual_songs),
            "mutual_songs": list(mutual_songs)
        })

    # Sort connections by the number of mutual songs (descending)
    sorted_connections = sorted(connections_with_song_count, key=lambda x: x['mutual_song_count'], reverse=True)

    return jsonify(sorted_connections), 200

@auth_bp.route("/connect/<int:id>", methods=["POST"])
def connect(id):
    # Assuming the `requesting_user_id` is passed in the request's JSON payload.
    requesting_user_id = request.json.get("requesting_user_id")
    
    if not requesting_user_id:
        return jsonify({"error": "Requesting user ID is required"}), 400

    # Retrieve the requesting user and the user to connect
    requesting_user = User.query.get(requesting_user_id)
    target_user = User.query.get(id)

    if not requesting_user or not target_user:
        return jsonify({"error": "One or both users not found"}), 404

    # Add target_user to the outgoing connections of requesting_user
    if not requesting_user.outgoing_connections.filter_by(id=target_user.id).first():
        requesting_user.outgoing_connections.append(target_user)
        db.session.commit()
        return jsonify({"message": "Connection added successfully"}), 200
    else:
        return jsonify({"message": "Connection already exists"}), 200
