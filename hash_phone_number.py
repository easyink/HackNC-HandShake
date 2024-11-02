#input would be something like 1XXXXXXXXXX

import hashlib

hash_obj = hashlib.blake2s(digest_size=4)
#digest size controls the length of the output hash. 
# we can make it shorter if needed

def generate_phone_hash(input_num):

	data = input_num.encode()
	hash_obj.update(data)

	hexhash = hash_obj.hexdigest()
	print(hexhash)


	
	return(hexhash)


generate_phone_hash("1234567890")

