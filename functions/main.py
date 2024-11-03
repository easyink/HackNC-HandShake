# Welcome to Cloud Functions for Firebase for Python!
# To get started, simply uncomment the below code or create your own.
# Deploy with `firebase deploy`

from firebase_functions import https_fn
from firebase_admin import initialize_app, firestore
from flask import jsonify

import hashlib

initialize_app()

# # input_json
# @https_fn.on_request()
# def on_request_example(req: https_fn.Request) -> https_fn.Response:
#     return https_fn.Response("Hello world!")

# # @functions.https.on_call



# @https_fn.on_call()
# def echoString(request):
#     #this is a test function
#     try:
#         # Log raw request data
#         print("Raw request data:", request)
        
#         # Extract 'text' field from the data payload
#         text = request.data.get('text', None)
        
#         if text is None:
#             print("No 'text' field found in request data.")
#             return {'error': 'No text provided'}, 400
        
#         print("Returning response:", text)
#         return {'response': text}  # Return as dictionary

#     except Exception as e:
#         print(f"Exception occurred: {e}")  # Log the exception for debugging
#         return {'error': 'An internal error occurred', 'details': str(e)}, 500
    
# @https_fn.on_call()
# def generate_phone_hash(input_num):
# 	#the input is a json object that looks basically like
# #   {
# #   	"data": {
# #     		"number": "1234567890"
# #   	}
# # 	}

# #	you will get back a new json object that looks like:
# 	# {
# 	#     "result": {
# 	#         "phone_hash_id": "dcde7a4c"
# 	#     }
# 	# }

# 	hash_obj = hashlib.blake2s(digest_size=4)

# 	# text = input_num.data.get('number', None)
# 	text = input_num

# 	data = text.encode()
# 	hash_obj.update(data)

# 	hexhash = hash_obj.hexdigest()
# 	# print(hexhash)

# 	return hexhash  # Return as dictionary

@https_fn.on_call()
def store_user_credential(input_json):


	phone_num = input_json.data.get('phoneNumber', None)
	name = input_json.data.get('name', None)
	
	
	hash_obj = hashlib.blake2s(digest_size=4)
	
	data = phone_num.encode()
	hash_obj.update(data)

	public_id = hash_obj.hexdigest()	
	
	# public_id = generate_phone_hash(phone_num)
	# print(public_id)
	biography =input_json.data.get('biography', None)
	interests =input_json.data.get('interests', None)
	handshake_card_frame =input_json.data.get('frame', None)
	handshake_card_color =input_json.data.get('color', "#FFFFFF")  # Default to white if not provided
	social_instagram =input_json.data.get('socialsInstagram', None)
	social_snapchat =input_json.data.get('socialsSnapchat', None)
	social_other =input_json.data.get('socialsOther', None)

	user_data_dict = {
		'name': name,
		'phone_number': phone_num,
		'biography': biography,
		'interests': interests,
		'handshake_card_frame': handshake_card_frame,
		'handshake_card_color': handshake_card_color,
		'social_instagram': social_instagram,
		'social_snapchat': social_snapchat,
		'social_other': social_other
	}
        # Initialize Firestore
	db = firestore.client()

	# Create or update the document in the "Users" collection
	new_document = db.collection("Users").document(public_id)
	new_document.set(user_data_dict)  # Use merge=True if necessary

	return {"message": "Succeeded!", "user_profile_id": public_id}

@https_fn.on_call()
def retrieve_credentials(input_pid_json):

	input_pid = input_pid_json.data.get("public_id", None)
	db = firestore.client()

	retrieve_ref = db.collection("Users").document(input_pid)
	retrieve_doc = retrieve_ref.get()
	return retrieve_doc.to_dict()

@https_fn.on_call()
def request_public_data(input_pid_json):
	#returns only safe public info like interests and stuff
	input_pid = input_pid_json.data.get("public_id", None)

	db = firestore.client()
	retrieve_db = db.collection("Users").document(input_pid)
	retrieve_get = retrieve_db.get()
	retrieve_ref = retrieve_get.to_dict()
	# retrieve_ref = retrieve_doc.to_dict()
	public_data:dict = {
		'public_id': input_pid,
		'name': retrieve_ref.get('name', None),
		'biography': retrieve_ref.get('biography', None),
		'interests': retrieve_ref.get('interests', None),
		'handshake_card_frame': retrieve_ref.get('frame',0),
		'handshake_card_color': retrieve_ref.get('color',"#FFFFFF"),
	}

	return public_data


def handshake_inquiry(request_id, sender_id, recipient_id):
	#push notification the request to the recipient
	print("sending to recipient phone!")

@https_fn.on_call()
def request_handshake(id_json):


	#generate a unique request id for this
	sender_id = id_json.data.get("sender_id")
	recipient_id = id_json.data.get("recipient_id")

	hash_obj = hashlib.blake2s(digest_size=4)

	data = (sender_id + recipient_id).encode()
	hash_obj.update(data)

	unique_id = hash_obj.hexdigest()	
	#pass request to recipient


	handshake_inquiry(unique_id, sender_id, recipient_id)

	return {"message": "Sucessfully sent request"}
