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

SESSION_USER_ID_TAG = 'user_id'
SESSION_USER_NAME_TAG = 'user_name'
SESSION_USER_TOKEN_TAG = 'user_token'

# -----------------------
# ACCOUNT USAGE FUNCTIONS
# -----------------------

def index():
	if SESSION_USER_ID_TAG in session:
		return escape(session[SESSION_USER_ID_TAG])
	else:
		return None

def index_token():
	if SESSION_USER_TOKEN_TAG in session:
		return escape(session[SESSION_USER_TOKEN_TAG])
	else:
		return None

def index_name():
	if SESSION_USER_NAME_TAG in session:
		return escape(session[SESSION_USER_NAME_TAG])
	else:
		return None

def session_login(user_id, access_token, name):
	print(">> RECEIVED LOGIN INFO: <id={} token={} name={}>".format(user_id, access_token, name))
	
	# add/update database entry for this user
	if database.get_user(user_id) is not None:
		database.update_user(user_id, access_token, name)
	else:
		database.create_user(user_id, access_token, name)
	
	if index():
		session_logout()
	
	session[SESSION_USER_ID_TAG] = user_id
	session[SESSION_USER_TOKEN_TAG] = access_token
	session[SESSION_USER_NAME_TAG] = name
	
	# update database information

def session_logout():
	if index():
		session.pop(SESSION_USER_ID_TAG, None)
	if index_token():
		session.pop(SESSION_USER_TOKEN_TAG, None)
	if index_name():
		session.pop(SESSION_USER_NAME_TAG, None)

