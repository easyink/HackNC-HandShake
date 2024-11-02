#User class for the server

class User:
	def __init__(self, name, phone_num, bio, interests, handshake_card, instagram, snapchat, other):
		self.name = name
		self.phone_number = phone_num
		self.bio = bio
		self.interests = interests
		self.handshake_card = handshake_card
		self.social_instagram = instagram
		self.social_snapchat = snapchat
		self.social_other = other

	