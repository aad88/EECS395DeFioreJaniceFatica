# native imports

# project imports

# external imports
try:
	from flask import Flask, render_template, request, redirect, session, escape
except ImportError:
	print("IMPORT ERROR: Need to install Flask via pip")
	sys.exit(1)
app = Flask(__name__)

# ---------------------------
# PROCESS PARAMETER VARIABLES
# ---------------------------

# base URL for redirects back to our application
REDIRECT_URL_BASE = 'http://www.presentsofmind.com'
# url for facebook login prompt
FACEBOOK_LOGIN_URL = "https://www.facebook.com/v2.8/dialog/oauth?client_id={}&redirect_uri={}"
# url for facebook logout prompt
FACEBOOK_LOGOUT_URL = ""

# ------------------------------
# FACEBOOK INTERACTION FUNCTIONS
# ------------------------------

# create a redirect URL for the given location
def create_redirect(template_loc):
	return REDIRECT_URL_BASE + template_loc

# get the name of the user logged into Facebook, if applicable
def index_name():
	# TODO
	return None

# get the email of the user logged into Facebook, if applicable
def index_email():
	# TODO
	return None

# launch the login process for this application via Facebook
def begin_login(key, template_loc):
	redirect_url = create_redirect(template_loc)
	login_url = FACEBOOK_LOGIN_URL.format(key, redirect_url)
	
	print("GIVEN FACEBOOK KEY OF {}".format(key))
	print("WILL REDIRECT TO {}".format(redirect_url))
	
	return redirect(login_url, 302)

# launch the logout process for this application via Facebook
def begin_logout(key, template_loc):
	# TODO
	return None

def grab_target_page(key, target):
	# TODO
	return None

