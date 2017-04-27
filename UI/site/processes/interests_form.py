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

def parse_label_info(form):
	# pull the label information from the form
	label = form.form['label']
	if label is None:
		return ''
	
	return label

def parse_age_info(form):
	# pull the age information as an int from the form
	age = form.form['age']
	if age == '':
		age = None
	else:
		age = int(age)
	return age

def parse_gender_info(form):
	# pull the gender information from the form
	gender = str(form.form['gender'])
	if gender == 'unspecified':
		return None
	
	return gender

def parse_hometown_info(form):
	# pull the hometown information from the form
	hometown = str(form.form['hometown'])
	if hometown == '':
		return None
	
	return hometown

def parse_interests_info(form):
	# pull the interests information from the form
	interests = str(form.form['interests'])
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

# ------------------------------
# FORM REQUEST PROCESSING METHOD
# ------------------------------

def info_from_form(form):
	info = {}
	
	info['label'] = parse_label_info(form)
	info['age'] = parse_age_info(form)
	info['gender'] = parse_gender_info(form)
	info['hometown'] = parse_hometown_info(form)
	info['interests'] = parse_interests_info(form)
	
	return info

