import firebase_admin
from firebase_admin import credentials,firestore

import hashlib

cred = credentials.Certificate('C:\Users\Dylan Lau\Documents\handshake-nc-firebase-adminsdk-atc6h-359f3c8352.json')
firebase_admin.initialize_app(cred)


db = firestore.client()



def generate_phone_hash(input_num):

	hash_obj = hashlib.blake2s(digest_size=4)
	#digest size controls the length of the output hash. 
	# we can make it shorter if needed
	
	data = input_num.encode()
	hash_obj.update(data)

	hexhash = hash_obj.hexdigest()
	print(hexhash)


	
	return(hexhash)