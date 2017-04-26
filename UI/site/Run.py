# native imports
import sys

# project imports
from processes import database, facebook, interests_form, pom_account, account

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
#FACEBOOK_ID = key(FACEBOOK_ID_KEY_NAME)
# grabbed facebook app secret from database
#FACEBOOK_SECRET = key(FACEBOOK_SECRET_KEY_NAME)

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
	'Facebook Login Process': (
		None,
		'/login/facebook',
		None
	),
	'Facebook Login Land': (
		None,
		'/login/facebook/finished',
		None
	),
	'Register': (
		'register',
		'/register',
		'Register for an Account - Presents of Mind'
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

# ------------------------
# TEMPLATE USAGE FUNCTIONS
# ------------------------

def create_nav_bar():
	nav_bar = []
	
	if pom_account.index():
		items = NAV_BAR_LOGGED_IN_ITEMS
	else:
		items = NAV_BAR_ITEMS
	
	for name in items:
		path = TEMPLATE_DIC[name][TEMPLATE_DIC_PATH_ENTRY]
		nav_bar.append((name, path))
	
	return nav_bar

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
		logged_in=pom_account.index(),
		
		# any other keyword arguments for Jinja
		**kw_args
	)

def redirect_to(template):
	return redirect(TEMPLATE_DIC[template][TEMPLATE_DIC_PATH_ENTRY], 302)

# ------------------------------------
# TEMPLATE ROUTING, RESPONSE FUNCTIONS
# ------------------------------------

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
		login_path=TEMPLATE_DIC['Login'][TEMPLATE_DIC_PATH_ENTRY]
	)

# LOGIN
@app.route(TEMPLATE_DIC['Login'][TEMPLATE_DIC_PATH_ENTRY], methods=['GET', 'POST'])
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
	user_id = request.json['userID']
	access_token = request.json['accessToken']
	first_name = request.json['firstName']
	
	print("{} {} {}".format(user_id, access_token, first_name))
	
	account.session_login(user_id, access_token, first_name)
	
	return "SUCCESS"

# FACEBOOK LOGIN LAND
#@app.route(TEMPLATE_DIC['Facebook Login Land'][TEMPLATE_DIC_PATH_ENTRY], methods=['POST')
#def login_l

# ACCOUNT
@app.route(TEMPLATE_DIC['Account'][TEMPLATE_DIC_PATH_ENTRY])
def account_template():
	user_id = None
	past_searches = None
	
	if pom_account.index():
		user_id = account.index()
		past_searches = database.get_searches_for_user(user_id)
	
	return setup_template(
		'Account',
		
		# template-specific fields
		username=user_id,
		past_searches=past_searches
	)

# SEARCH
@app.route(TEMPLATE_DIC['Search'][TEMPLATE_DIC_PATH_ENTRY])
def search_template():
	return setup_template(
		'Search',
		
		# template-specific fields
		login_redirect_path=TEMPLATE_DIC['Facebook Logout Launch'][TEMPLATE_DIC_PATH_ENTRY],
		intermediate_search_path=TEMPLATE_DIC['Manual Form'][TEMPLATE_DIC_PATH_ENTRY]
	)

# MANUAL FORM
@app.route(TEMPLATE_DIC['Manual Form'][TEMPLATE_DIC_PATH_ENTRY], methods=['GET', 'POST'])
def manual_form_template():
	if request.method == 'GET':
		return setup_template(
			'Manual Form',
			
			# template-specific fields
			submission_path=TEMPLATE_DIC['Manual Form'][TEMPLATE_DIC_PATH_ENTRY],
			bad_entry=False,
			prev_label='',
			prev_age=None,
			prev_gender='unspecified',
			prev_hometown='',
			prev_interests=''
		)
	elif request.method == 'POST':
		#username = pom_account.index()
		#interests_form.process_req(username, request)
		try:
			username = pom_account.index()
			interests_form.process_req(username, request)
		except Exception:
			return setup_template(
				'Manual Form',
			
				# template-specific fields
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
		if pom_account.index():
			username = pom_account.index()
			most_recent_search = database.get_most_recent_search(username)
		
		return setup_template(
			'Results',
			
			# template-specific fields
			results=most_recent_search
		)

# LOGOUT
@app.route(TEMPLATE_DIC['Logout'][TEMPLATE_DIC_PATH_ENTRY])
def logout_template():
	return setup_template(
		'Logout',
		
		# template-specific fields
		logout_redirect_path=TEMPLATE_DIC['Facebook Logout Process'][TEMPLATE_DIC_PATH_ENTRY]
	)

# FACEBOOK LOGOUT PROCESS
@app.route(TEMPLATE_DIC['Facebook Logout Process'][TEMPLATE_DIC_PATH_ENTRY], methods=['POST'])
def logout_launch_redirect():
	account.session_logout()
	
	return "SUCCESS"

# -------------------------------------
# MAIN PROCEDURE - START UP APPLICATION
# -------------------------------------

if __name__ == '__main__':
	app.secret_key = APP_KEY
	
	app.run()

