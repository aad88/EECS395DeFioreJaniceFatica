# native imports

# project imports
import database

# external imports
try:
	from flask import session, escape
except ImportError:
	print("IMPORT ERROR: Need to install Flask via pip")
	sys.exit(1)

# -------------------------------------
# USERNAME, PASSWORD REQUIREMENT VALUES
# -------------------------------------

SESSION_USER_TAG = 'username'

# -----------------------
# ACCOUNT USAGE FUNCTIONS
# -----------------------

def index():
	if SESSION_USER_TAG in session:
		return escape(session[SESSION_USER_TAG])
	else:
		return None

def session_login(user_id, access_token, first_name):
	print(">> RECEIVED LOGIN INFO: <id={} token={}>".format(user_id, access_token))
	
	# add/update database entry for this user
	if database.user_exists(user_id):
		database.update_user(user_id, access_token, first_name)
	else:
		database.create_user(user_id, access_token, first_name)
	
	if index():
		session.pop(SESSION_USER_TAG, None)
	
	session[SESSION_USER_TAG] = user_id
	
	# update database information

def session_logout():
	if index():
		session.pop(SESSION_USER_TAG, None)

