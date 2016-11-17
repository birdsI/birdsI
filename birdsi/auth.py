#
# auth.py
# This file contains the class definitions needed for a user to register
# and login
#

import bcrypt
import re
import db

class UserManager:
	"""Handles user registration, and authentication"""

	@staticmethod
	def valid_email(email, email_repeat):
		# Checks if emails match and for regex match
		verifyEmail = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)
		if email == email_repeat and verifyEmail != None:
			return True
		
		return False			

	@staticmethod
	def valid_password(password, password_repeat):
		# Checks if passwords match, longer than 6 chars, contains uppercase 
		# and lower case letter, and a number
		verifyPassword = re.match('^(?=.{6,})(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).*$', password)
		print(verifyPassword)
		if password == password_repeat and verifyPassword != None:
			return True

		return False 
		
	@staticmethod
	def register(username, email, email_repeat, password, password_repeat):
		# This method requires the user to enter email and password twice
		# to ensure correctness. 
		#
		# Returns user if successful, None otherwise
		# 
		# Currently, no validation email is being sent to the given email
		
		if UserManager.valid_email(email, email_repeat) \
			and UserManager.valid_password(password, password_repeat) \
			and username:
			# Email valid, password valid, name exists, good to go
			password_hex_bytes = password.encode('utf-8')
			hashed_password = bcrypt.hashpw(password_hex_bytes, bcrypt.gensalt())

			# Ready to store in DB
			db.insertUser(email, username, hashed_password)
			user = db.retrieveUser(email)
			if user:
				return user

		return None

	@staticmethod
	def login(email, password):
		# Returns True if successful, False if not
		# 

		# Query DB for user attempting to log in
		user = db.retrieveUser(email)
		
		# Need to check if user is returned (email exists) and password
		# matches the one stored for that user
		password_hex_bytes = password.encode('utf-8')
		if user is not None:

			retrieved_password = user[3].encode('utf-8')
			if bcrypt.hashpw(password_hex_bytes, retrieved_password) == retrieved_password:
			# password is 4th element in tuple
				return user

		return None			
