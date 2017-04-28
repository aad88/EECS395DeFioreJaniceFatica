# native imports
import sys

# project imports
from processes import database, account, search_query

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

# nav bar listing (not logged in)
NAV_BAR_ITEMS = (
	'Home',
	'Login'
)
# nav bar listing (logged in)
NAV_BAR_LOGGED_IN_ITEMS = (
	'Home',
	'Account',
	'Search',
	'Logout'
)

# template dictionary (template file name, path, page title)
TEMPLATE_DIC = {
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
	'Facebook Login Process': (
		None,
		'/login/facebook',
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
	'Facebook Search Process': (
		None,
		'/search/facebook',
		None
	),
	'Manual Form': (
		'manual_form',
		'/form',
		'Search Form - Presents of Mind'
	),
	'Results': (
		'results',
		'/results',
		'Query Results - Presents of Mind'
	),
	'Logout': (
		'logout',
		'/logout',
		'Logout via Facebook - Presents of Mind'
	),
	'Facebook Logout Process': (
		None,
		'/logout/facebook',
		None
	)
}

# template dictionary file name index
TEMPLATE_DIC_NAME_ENTRY = 0
# template dictionary page path index
TEMPLATE_DIC_PATH_ENTRY = 1
# template dictionary page title index
TEMPLATE_DIC_PAGE_HEAD_ENTRY = 2

# ------------------------
# TEMPLATE USAGE FUNCTIONS
# ------------------------

# creates a navigation bar for use by the wrapper template
def create_nav_bar():
	nav_bar = []
	
	# choose items to display depending on the user's login status
	if account.index():
		items = NAV_BAR_LOGGED_IN_ITEMS
	else:
		items = NAV_BAR_ITEMS
	
	# map each navigation item provided
	for name in items:
		path = TEMPLATE_DIC[name][TEMPLATE_DIC_PATH_ENTRY]
		nav_bar.append((name, path))
	
	return nav_bar

# wrapper for 'render_template()' with constant keyword inclusions
def setup_template(template, **kw_args):
	return render_template(
		# template name, from dictionary
		TEMPLATE_DIC[template][TEMPLATE_DIC_NAME_ENTRY],
		
		# page information arguments
		page_header=TEMPLATE_DIC[template][TEMPLATE_DIC_PAGE_HEAD_ENTRY],
		page_path=TEMPLATE_DIC[template][TEMPLATE_DIC_PATH_ENTRY],
		
		# page wrapper arguments
		nav_bar=create_nav_bar(),
		current_nav=template,
		
		# login status arguments
		logged_in=account.index(),
		
		# any other keyword arguments for Jinja
		**kw_args
	)

# wrapper for 'redirect_to()' that grabs template info and uses constant redirect code
def redirect_to(template):
	return redirect(TEMPLATE_DIC[template][TEMPLATE_DIC_PATH_ENTRY], 302)

# ------------------------------------
# TEMPLATE ROUTING, RESPONSE FUNCTIONS
# ------------------------------------

# HOME
@app.route(TEMPLATE_DIC['Home'][TEMPLATE_DIC_PATH_ENTRY], methods=['GET'])
def home_template():
	if request.method == 'GET':
		return setup_template(
			'Home',
		
			# template-specific fields
			login_path=TEMPLATE_DIC['Login'][TEMPLATE_DIC_PATH_ENTRY]
		)

# LOGIN
@app.route(TEMPLATE_DIC['Login'][TEMPLATE_DIC_PATH_ENTRY], methods=['GET'])
def login_template():
	if request.method == 'GET':
		return setup_template(
			'Login',
			
			# template-specific fields
			login_redirect_path=TEMPLATE_DIC['Facebook Login Process'][TEMPLATE_DIC_PATH_ENTRY]
		)

# FACEBOOK LOGIN PROCESS
@app.route(TEMPLATE_DIC['Facebook Login Process'][TEMPLATE_DIC_PATH_ENTRY], methods=['POST'])
def login_launch_process():
	if request.method == 'POST':
		# relay login event to server console
		print("LOGIN STATUS: {}".format(request.json['status']))
	
		# grab user information from request
		user_id = request.json['userID']
		access_token = request.json['accessToken']
		name = request.json['name']
	
		# use Flask's session cookies to record login status
		account.session_login(user_id, access_token, name)
	
		# respond to ajax call
		return 'SUCCESS'

# ACCOUNT
@app.route(TEMPLATE_DIC['Account'][TEMPLATE_DIC_PATH_ENTRY], methods=['GET'])
def account_template():
	if request.method == 'GET':
		# initialize user information
		user_id = None
		user_name = None
		past_searches = None
	
		# if logged in, grab obtainable information from the user
		if account.index():
			user_id = account.index()
			user_name = account.index_name()
			past_searches = database.get_searches_for_user(user_id)
	
		# construct the template
		return setup_template(
			'Account',
		
			# template-specific fields
			username=user_name,
			past_searches=past_searches
		)

# SEARCH
@app.route(TEMPLATE_DIC['Search'][TEMPLATE_DIC_PATH_ENTRY], methods=['GET'])
def search_template():
	if request.method == 'GET':
		return setup_template(
			'Search',
			
			# template-specific fields
			login_redirect_path=TEMPLATE_DIC['Login'][TEMPLATE_DIC_PATH_ENTRY],
			intermediate_search_path=TEMPLATE_DIC['Manual Form'][TEMPLATE_DIC_PATH_ENTRY],
			access_token=account.index_token()
		)

# FACEBOOK SEARCH PROCESS
@app.route(TEMPLATE_DIC['Facebook Search Process'][TEMPLATE_DIC_PATH_ENTRY], methods=['POST'])
def search_launch_process():
	if request.method == 'POST':
		# process the search on the user's behalf
		user_id = account.index()
		search_query.process_facebook_query(user_id, request.json)
		
		# respond to ajax call
		return 'SUCCESS'

# MANUAL FORM
@app.route(TEMPLATE_DIC['Manual Form'][TEMPLATE_DIC_PATH_ENTRY], methods=['GET', 'POST'])
def manual_form_template():
	if request.method == 'GET':
		return setup_template(
			'Manual Form',
			
			# template-specific fields
			login_redirect_path=TEMPLATE_DIC['Login'][TEMPLATE_DIC_PATH_ENTRY],
			submission_path=TEMPLATE_DIC['Manual Form'][TEMPLATE_DIC_PATH_ENTRY],
			bad_entry=False,
			prev_label='',
			prev_age=None,
			prev_gender='unspecified',
			prev_hometown='',
			prev_interests=''
		)
	elif request.method == 'POST':
		#user_id = account.index()
		#search_query.process_manual_query(user_id, request)
		
		# attempt to process the search from the given information
		try:
			user_id = account.index()
			search_query.process_manual_query(user_id, request)
		except Exception:
			# if something went wrong with the search, bounce back to the search page
			return setup_template(
				'Manual Form',
			
				# template-specific fields
				login_redirect_path=TEMPLATE_DIC['Login'][TEMPLATE_DIC_PATH_ENTRY],
				submission_path=TEMPLATE_DIC['Manual Form'][TEMPLATE_DIC_PATH_ENTRY],
				bad_entry=True,
				prev_label = request.form['label'],
				prev_age=request.form['age'],
				prev_gender=request.form['gender'],
				prev_hometown=request.form['hometown'],
				prev_interests=request.form['interests']
			)
		
		return redirect_to('Results')

# RESULTS
@app.route(TEMPLATE_DIC['Results'][TEMPLATE_DIC_PATH_ENTRY], methods=['GET'])
def results_template():
	if request.method == 'GET':
		# if logged in, results are the most recent search performed
		if account.index():
			user_id = account.index()
			most_recent_search = database.get_most_recent_search(user_id)
		else:
			most_recent_search = None
		
		# construct the template
		return setup_template(
			'Results',
			
			# template-specific fields
			login_redirect_path=TEMPLATE_DIC['Login'][TEMPLATE_DIC_PATH_ENTRY],
			results=most_recent_search
		)

# LOGOUT
@app.route(TEMPLATE_DIC['Logout'][TEMPLATE_DIC_PATH_ENTRY], methods=['GET'])
def logout_template():
	return setup_template(
		'Logout',
		
		# template-specific fields
		logout_redirect_path=TEMPLATE_DIC['Facebook Logout Process'][TEMPLATE_DIC_PATH_ENTRY],
		access_token=account.index_token()
	)

# FACEBOOK LOGOUT PROCESS
@app.route(TEMPLATE_DIC['Facebook Logout Process'][TEMPLATE_DIC_PATH_ENTRY], methods=['POST'])
def logout_launch_redirect():
	# deconstruct login session in Flask's session cookies
	account.session_logout()
	
	# respond to ajax call
	return 'SUCCESS'

# -------------------------------------
# MAIN PROCEDURE - START UP APPLICATION
# -------------------------------------

if __name__ == '__main__':
	# attach the key for this app
	app.secret_key = APP_KEY
	
	# start the app
	app.run()

