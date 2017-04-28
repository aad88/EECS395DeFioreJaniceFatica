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

# session name for user's id
SESSION_USER_ID_TAG = 'user_id'
# session name for user's name
SESSION_USER_NAME_TAG = 'user_name'
# session name for user's token
SESSION_USER_TOKEN_TAG = 'user_token'

# -----------------------
# ACCOUNT USAGE FUNCTIONS
# -----------------------

# get the user's id from the current session
def index():
	if SESSION_USER_ID_TAG in session:
		return escape(session[SESSION_USER_ID_TAG])
	else:
		return None

# get the user's access token from the current session
def index_token():
	if SESSION_USER_TOKEN_TAG in session:
		return escape(session[SESSION_USER_TOKEN_TAG])
	else:
		return None

# get the user's name from the current session
def index_name():
	if SESSION_USER_NAME_TAG in session:
		return escape(session[SESSION_USER_NAME_TAG])
	else:
		return None

# have the session cookies record a login for a specified user
def session_login(user_id, access_token, name):
	# relay login request to server's console
	print(">> RECEIVED LOGIN INFO: <id={} token={} name={}>".format(user_id, access_token, name))
	
	# create/update user information in the database, as applicable
	if database.get_user(user_id) is not None:
		database.update_user(user_id, access_token, name)
	else:
		database.create_user(user_id, access_token, name)
	
	# if the session already contains a login, clear it
	if index():
		session_logout()
	
	# write user's information to the session
	session[SESSION_USER_ID_TAG] = user_id
	session[SESSION_USER_TOKEN_TAG] = access_token
	session[SESSION_USER_NAME_TAG] = name

# have the session cookies clear the login status for a specified user
def session_logout():
	# remove the user's id
	if index():
		session.pop(SESSION_USER_ID_TAG, None)
	
	# remove the user's access token
	if index_token():
		session.pop(SESSION_USER_TOKEN_TAG, None)
	
	# remove the user's name
	if index_name():
		session.pop(SESSION_USER_NAME_TAG, None)

