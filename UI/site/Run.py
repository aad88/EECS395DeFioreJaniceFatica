# native imports
import sys

# project imports
from processes import database, facebook

# external imports
try:
	from flask import Flask, render_template, request, redirect, session, escape
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
# facebook app key
FACEBOOK_KEY_NAME = 'fb_app_key'

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
# grabbed facebook app key from database
FACEBOOK_KEY = key(FACEBOOK_KEY_NAME)

# ------------------------------
# APPLICATION LAYOUT DEFINITIONS
# ------------------------------

# nav bar listing
NAV_BAR_ITEMS = (
	'Home',
	'Search Anonymously',
	'Login'
)

NAV_BAR_LOGGED_IN_ITEMS = (
	'Home',
	'Account',
	'Search',
	'Logout'
)

# template dictionary
TEMPLATE_DIC = {
	'Test Page': (
		'test',
		'/test',
		'PoM TEST PAGE'
	),
	'Home': (
		'home',
		'/',
		'Home - Presents of Mind'
	),
	'Login': (
		'login',
		'/login',
		'Login via Facebook - Presents of Mind'
	),
	'Facebook Login Launch': (
		None,
		'/login/facebook',
		None
	),
	'Facebook Login Land': (
		None,
		'/login/facebook/finished',
		None
	),
	'Account': (
		'account',
		'/account',
		'Your Account - Presents of Mind'
	),
	'Search': (
		'search',
		'/search',
		'Search - Presents of Mind'
	),
	'Logout': (
		'logout',
		'/logout',
		'Logout via Facebook - Presents of Mind'
	),
	'Facebook Logout Launch': (
		None,
		'/logout/facebook',
		None
	),
	'Facebook Logout Land': (
		None,
		'/logout/facebook/finished',
		None
	)
}

# template dictionary aliases
TEMPLATE_DIC['Search Anonymously'] = TEMPLATE_DIC['Search']

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
	
		# common fields
		nav_bar=create_nav_bar(),
		current_nav=template,
		page_header=TEMPLATE_DIC[template][TEMPLATE_DIC_PAGE_HEAD_ENTRY],
	
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
@app.route(TEMPLATE_DIC['Test Page'][TEMPLATE_DIC_PATH_ENTRY])
def test_page_template():
	return setup_template(
		'Test Page',
		
		# template-specific fields
		dummy=''
	)

# HOME
@app.route(TEMPLATE_DIC['Home'][TEMPLATE_DIC_PATH_ENTRY])
def home_template():
	return setup_template(
		'Home',
		
		# template-specific fields
		login_path=TEMPLATE_DIC['Login'][TEMPLATE_DIC_PATH_ENTRY],
		logged_in=index()
	)

# LOGIN
@app.route(TEMPLATE_DIC['Login'][TEMPLATE_DIC_PATH_ENTRY])
def login_template():
	return setup_template(
		'Login',
		
		# template-specific fields
		login_redirect_path=TEMPLATE_DIC['Facebook Login Launch'][TEMPLATE_DIC_PATH_ENTRY]
	)

# FACEBOOK LOGIN LAUNCH
@app.route(TEMPLATE_DIC['Facebook Login Launch'][TEMPLATE_DIC_PATH_ENTRY])
def login_launch_redirect():
	# TODO: remove
	login('test', 'test')
	
	return facebook.begin_login(FACEBOOK_KEY)

# FACEBOOK LOGIN LAND
@app.route(TEMPLATE_DIC['Facebook Login Land'][TEMPLATE_DIC_PATH_ENTRY])
def login_land_redirect():
	return redirect_to('Account')

# ACCOUNT
@app.route(TEMPLATE_DIC['Account'][TEMPLATE_DIC_PATH_ENTRY])
def account_template():
	username = None
	past_searches = None
	
	if index():
		username = index()
		past_searches = ['Alex', 'Lexi', 'Zach']
	
	return setup_template(
		'Account',
		
		# template-specific fields
		username=username,
		past_searches=past_searches
	)

# SEARCH
@app.route(TEMPLATE_DIC['Search'][TEMPLATE_DIC_PATH_ENTRY])
def search_template():
	return setup_template(
		'Search',
		
		# template-specific fields
		facebook_search_path=TEMPLATE_DIC['Search'][TEMPLATE_DIC_PATH_ENTRY],
		logged_in=index()
	)

# LOGOUT
@app.route(TEMPLATE_DIC['Logout'][TEMPLATE_DIC_PATH_ENTRY])
def logout_templaten():
	return setup_template(
		'Logout',
		
		# template-specific fields
		login_redirect_path=TEMPLATE_DIC['Facebook Logout Launch'][TEMPLATE_DIC_PATH_ENTRY]
	)

# FACEBOOK LOGOUT LAUNCH
@app.route(TEMPLATE_DIC['Facebook Logout Launch'][TEMPLATE_DIC_PATH_ENTRY])
def logout_launch_redirect():
	# TODO: remove
	logout()
	
	return facebook.begin_logout(FACEBOOK_KEY)

# FACEBOOK LOGOUT LAND
@app.route(TEMPLATE_DIC['Facebook Logout Land'][TEMPLATE_DIC_PATH_ENTRY])
def logout_land_redirect():
	return redirect_to('Login')

# -------------------------------------
# MAIN PROCEDURE - START UP APPLICATION
# -------------------------------------

if __name__ == '__main__':
	app.secret_key = APP_KEY
	
	app.run()

