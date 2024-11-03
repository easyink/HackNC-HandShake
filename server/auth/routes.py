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