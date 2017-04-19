# native imports
import os
import sys

# project imports
from processes import database, facebook

# external imports
try:
	from flask import Flask, render_template, request, redirect, session, escape, send_from_directory
except ImportError:
	print("IMPORT ERROR: Need to install Flask via pip")
	sys.exit(1)

app = Flask(__name__)

# ------------------------------
# APPLICATION RESOURCE VARIABLES
# ------------------------------

# database credentials file
DB_CREDS_FILE = 'db_creds.txt'
# application key, for cookies
APP_KEY_NAME = 'app_key'
# facebook app id
FACEBOOK_ID_KEY_NAME = 'fb_app_id'
# facebook app secret
FACEBOOK_SECRET_KEY_NAME = 'fb_app_secret'

# ---------------------------
# DATABASE-ORIENTED VARIABLES
# ---------------------------

# database session
DB_SESSION = database.connect_with_cred_file(DB_CREDS_FILE)

# wrapper method for using the database to gey a requested key
def key(name):
	return database.get_key(name)

# grabbed application key from database
APP_KEY = key(APP_KEY_NAME)
# grabbed facebook app id from database
FACEBOOK_ID = key(FACEBOOK_ID_KEY_NAME)
# grabbed facebook app secret from database
FACEBOOK_SECRET = key(FACEBOOK_SECRET_KEY_NAME)

# ------------------------------
# APPLICATION LAYOUT DEFINITIONS
# ------------------------------

# nav bar listing
NAV_BAR_ITEMS = (
	'Test Page'
)

NAV_BAR_LOGGED_IN_ITEMS = (
	'Test Page'
)

# template dictionary
TEMPLATE_DIC = {
	'Test Page': (
		'test',
		'/test',
		'PoM TEST PAGE'
	)
}

# template dictionary entry index constants
TEMPLATE_DIC_NAME_ENTRY = 0
TEMPLATE_DIC_PATH_ENTRY = 1
TEMPLATE_DIC_PAGE_HEAD_ENTRY = 2

# ----------------
# SERVER FUNCTIONS
# ----------------

def setup_template(template, **kw_args):
	return render_template(
		# template name, from dictionary
		TEMPLATE_DIC[template][TEMPLATE_DIC_NAME_ENTRY],
		
		# any other keyword arguments for Jinja
		**kw_args
	)

def redirect_to(template):
	return redirect(TEMPLATE_DIC[template][TEMPLATE_DIC_PATH_ENTRY], 302)

def create_nav_bar():
	nav_bar = []
	
	if index():
		items = NAV_BAR_LOGGED_IN_ITEMS
	else:
		items = NAV_BAR_ITEMS
	
	for name in items:
		path = TEMPLATE_DIC[name][TEMPLATE_DIC_PATH_ENTRY]
		nav_bar.append((name, path))
	
	return nav_bar

# ----------------------------
# ACCOUNT MANAGEMENT FUNCTIONS
# ----------------------------

# TODO: outdated with Facebook integration
def index():
	if 'username' in session:
		return escape(session['username'])
	else:
		return None

# TODO: outdated with Facebook integration
def login(username, password):
	if index():
		logout()
	
	print(">> RECEIVED LOGIN REQUEST FOR <user={} pass={}>".format(username, password))
	session['username'] = username

# TODO: outdated with Facebook integration
def logout():
	if index():
		print(">> RECEIVED LOGOUT REQUEST FOR <user={}>".format(index()))
		session.pop('username', None)

# ------------------
# TEMPLATE FUNCTIONS
# ------------------

# TEST PAGE
@app.route(TEMPLATE_DIC['Test Page'][TEMPLATE_DIC_PATH_ENTRY], methods=['GET'])
def test_page_template():
	if request.method == 'GET':
		return setup_template(
			'Test Page',
		
			# template-specific fields
			dummy=''
		)

# -------------------------------------
# MAIN PROCEDURE - START UP APPLICATION
# -------------------------------------

if __name__ == '__main__':
	app.secret_key = APP_KEY
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)

