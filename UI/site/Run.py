# native imports

# project imports

# external imports
from flask import Flask, render_template, request, redirect, session, escape
app = Flask(__name__)

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
		'Login - Presents of Mind'
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
		None,
		'/logout',
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

def index():
	if 'username' in session:
		return escape(session['username'])
	else:
		return None

# TODO: Database integartion for password check
def login(username, password):
	if index():
		logout()
	
	print(">> RECEIVED LOGIN REQUEST FOR <user={} pass={}>".format(username, password))
	session['username'] = username

def logout():
	if index():
		print(">> RECEIVED LOGOUT REQUEST FOR <user={}>".format(index()))
		session.pop('username', None)

# ------------------------
# TEMPLATE FUNCTIONALITIES
# ------------------------

# TEST PAGE
@app.route(TEMPLATE_DIC['Test Page'][TEMPLATE_DIC_PATH_ENTRY])
def test_page_template():
	return render_template(
		# template name, from dictionary
		TEMPLATE_DIC['Test Page'][TEMPLATE_DIC_NAME_ENTRY],
		
		# common fields
		nav_bar=create_nav_bar(),
		current_nav='Test Page',
		page_header=TEMPLATE_DIC['Test Page'][TEMPLATE_DIC_PAGE_HEAD_ENTRY],
		
		# template-specific fields
		dummy=''
	)

# HOME
@app.route(TEMPLATE_DIC['Home'][TEMPLATE_DIC_PATH_ENTRY])
def home_template():
	return render_template(
		# template name, from dictionary
		TEMPLATE_DIC['Home'][TEMPLATE_DIC_NAME_ENTRY],
		
		# common fields
		nav_bar=create_nav_bar(),
		current_nav='Home',
		page_header=TEMPLATE_DIC['Home'][TEMPLATE_DIC_PAGE_HEAD_ENTRY],
		
		# template-specific fields
		dummy=''
	)

# LOGIN
@app.route(TEMPLATE_DIC['Login'][TEMPLATE_DIC_PATH_ENTRY])
def login_template():
	return render_template(
		# template name, from dictionary
		TEMPLATE_DIC['Login'][TEMPLATE_DIC_NAME_ENTRY],
		
		# common fields
		nav_bar=create_nav_bar(),
		current_nav='Login',
		page_header=TEMPLATE_DIC['Login'][TEMPLATE_DIC_PAGE_HEAD_ENTRY],
		
		# template-specific fields
		login_path=TEMPLATE_DIC['Login'][TEMPLATE_DIC_PATH_ENTRY]
	)

# LOGIN, with login submission
@app.route(TEMPLATE_DIC['Login'][TEMPLATE_DIC_PATH_ENTRY], methods=['POST'])
def login_template_with_login_action():
	username = request.form['username']
	password = request.form['password']
	login(username, password)
	
	return redirect(TEMPLATE_DIC['Account'][TEMPLATE_DIC_PATH_ENTRY], 302)

# ACCOUNT
@app.route(TEMPLATE_DIC['Account'][TEMPLATE_DIC_PATH_ENTRY])
def account_template():
	username = None
	past_searches = None
	
	if index():
		username = index()
		past_searches = ['Claire']
	
	return render_template(
		# template name, from dictionary
		TEMPLATE_DIC['Account'][TEMPLATE_DIC_NAME_ENTRY],
		
		# common fields
		nav_bar=create_nav_bar(),
		current_nav='Account',
		page_header=TEMPLATE_DIC['Account'][TEMPLATE_DIC_PAGE_HEAD_ENTRY],
		
		# template-specific fields
		username=username,
		past_searches=past_searches
	)

# SEARCH
@app.route(TEMPLATE_DIC['Search'][TEMPLATE_DIC_PATH_ENTRY])
def search_template():
	return render_template(
		# template name, from dictionary
		TEMPLATE_DIC['Search'][TEMPLATE_DIC_NAME_ENTRY],
		
		# common fields
		nav_bar=create_nav_bar(),
		current_nav='Search',
		page_header=TEMPLATE_DIC['Search'][TEMPLATE_DIC_PAGE_HEAD_ENTRY],
		
		# template-specific fields
		dummy=''
	)

@app.route(TEMPLATE_DIC['Logout'][TEMPLATE_DIC_PATH_ENTRY], methods=['GET'])
def logout_template_with_logout_action():
	logout()
	
	return redirect(TEMPLATE_DIC['Home'][TEMPLATE_DIC_PATH_ENTRY], 302)

app.secret_key = 'AAX1$*.d/21532&HSD*[]ASD'
if __name__ == '__main__':
	app.run()

