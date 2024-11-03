# Welcome to Cloud Functions for Firebase for Python!
# To get started, simply uncomment the below code or create your own.
# Deploy with `firebase deploy`

from firebase_functions import https_fn
from firebase_admin import initialize_app
from flask import jsonify

initialize_app()


@https_fn.on_request()
def on_request_example(req: https_fn.Request) -> https_fn.Response:
    return https_fn.Response("Hello world!")

# @functions.https.on_call

@https_fn.on_call()
def echoString(request):
    try:
        # Log raw request data
        print("Raw request data:", request)
        
        # Extract 'text' field from the data payload
        text = request.data.get('text', None)
        
        if text is None:
            print("No 'text' field found in request data.")
            return {'error': 'No text provided'}, 400
        
        print("Returning response:", text)
        return {'response': text}  # Return as dictionary

    except Exception as e:
        print(f"Exception occurred: {e}")  # Log the exception for debugging
        return {'error': 'An internal error occurred', 'details': str(e)}, 500