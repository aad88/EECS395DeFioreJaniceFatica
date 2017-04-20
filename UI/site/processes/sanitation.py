# native imports

# project imports

# external imports


# ------------------------
# ACCEPTED CHARACTER LISTS
# ------------------------

USERNAME_CHARS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
PASSWORD_CHARS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*-_+=,.'

# --------------------------
# SANITATION CHECK FUNCTIONS
# --------------------------

def is_sanitary_username(username):
	for char in username:
		if char not in USERNAME_CHARS:
			return False
	
	return True

def is_sanitary_password(password):
	for char in password:
		if char not in PASSWORD_CHARS:
			return False
	
	return True

