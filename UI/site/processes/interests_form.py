# native imports
import string

# project imports

# external imports
try:
	from flask import request
except ImportError:
	print("IMPORT ERROR: Need to install Flask via pip")
	sys.exit(1)

# ----------------
# GLOBAL VARIABLES
# ----------------

INTERESTS_WHITESPACE_TO_REMOVE = string.whitespace.replace('\n', '').replace(' ', '')

# -------------
# PARSE METHODS
# -------------

def parse_age_info(req):
	# pull the age information as an int from the form
	age = req.form['age']
	if age == '':
		age = None
	else:
		age = int(age)
	return age

def parse_gender_info(req):
	# pull the gender information from the form
	gender = str(req.form['gender'])
	if gender == 'unspecified':
		return None
	
	return gender

def parse_hometown_info(req):
	# pull the hometown information from the form
	hometown = str(req.form['hometown'])
	if hometown == '':
		return None
	
	return hometown

def parse_interests_info(req):
	# pull the interests information from the form
	interests = str(req.form['interests'])
	if interests == '':
		return None
	
	# clean interests input
	interests = interests.strip(INTERESTS_WHITESPACE_TO_REMOVE)
	interests = interests.replace('\r', '')
	
	# create a list of the interests
	interest_list = []
	for interest in interests.split('\n'):
		if interest != '':
			interest_list.append(interest)
	
	return interest_list

# --------------------------
# REQUEST PROCESSING METHODS
# --------------------------

def info_from_req(req):
	info = {}
	
	info['age'] = parse_age_info(req)
	info['gender'] = parse_gender_info(req)
	info['hometown'] = parse_hometown_info(req)
	info['interests'] = parse_interests_info(req)
	
	return info



