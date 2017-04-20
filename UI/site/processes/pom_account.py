# native imports

# project imports
import database
import sanitation

# external imports
try:
	from flask import session, escape
except ImportError:
	print("IMPORT ERROR: Need to install Flask via pip")
	sys.exit(1)

# -------------------------------------
# USERNAME, PASSWORD REQUIREMENT VALUES
# -------------------------------------

USERNAME_MIN_LEN = 6
USERNAME_MAX_LEN = 20
PASSWORD_MIN_LEN = 8
PASSWORD_MAX_LEN = 40

# --------------------------
# INPUT VALIDATION FUNCTIONS
# --------------------------

def is_valid_username(username):
	length = len(username)
	if length < USERNAME_MIN_LEN or USERNAME_MAX_LEN < length:
		return False
	
	return sanitation.is_sanitary_username(username)

def is_valid_password(password, confirmation=None):
	length = len(password)
	if length < PASSWORD_MIN_LEN or PASSWORD_MAX_LEN < length:
		return False
	
	if not sanitation.is_sanitary_password(password):
		return False
	
	return True if confirmation is None else password == confirmation

# -----------------------
# ACCOUNT USAGE FUNCTIONS
# -----------------------

def index():
	if 'username' in session:
		return escape(session['username'])
	else:
		return None

def login(username, password):
	print(">> RECEIVED LOGIN REQUEST FOR <user={} pass={}>".format(username, password))
	
	if not (is_valid_username(username) and is_valid_password(password)):
		return False
	
	if database.is_valid_login(username, password):
		print(">> LOGIN REQUEST GRANTED FOR <user={} pass={}>".format(username, password))
		if index():
			logout()
		session['username'] = username
		return True
	else:
		return False

def logout():
	if index():
		print(">> RECEIVED LOGOUT REQUEST FOR <user={}>".format(index()))
		print(">> LOGOUT REQUEST GRANTED FOR <user={}>".format(index()))
		session.pop('username', None)

def attempt_create_account(username, password):
	if database.user_exists(username):
		return False
	
	database.create_user(username, password)
	if not login(username, password):
		raise Exception
	
	return True

