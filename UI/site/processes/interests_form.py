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

# whitespace to remove from the inputs in the form's fields
INTERESTS_WHITESPACE_TO_REMOVE = string.whitespace.replace('\n', '').replace(' ', '')

# -------------
# PARSE METHODS
# -------------

# pull the label information from the form
def parse_label_info(form):
	label = form.form['label']
	if label is None:
		return ''
	
	return label

# pull the age information as an int from the form
def parse_age_info(form):
	age = form.form['age']
	if age == '':
		age = None
	else:
		age = int(age)
	return age

# pull the gender information from the form
def parse_gender_info(form):
	gender = str(form.form['gender'])
	if gender == 'unspecified':
		return None
	
	return gender

# pull the hometown information from the form
def parse_hometown_info(form):
	hometown = str(form.form['hometown'])
	if hometown == '':
		return None
	
	return hometown

# pull the interests information from the form
def parse_interests_info(form):
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
	# parse out each piece of information from the form
	info = {}
	info['label'] = parse_label_info(form)
	info['age'] = parse_age_info(form)
	info['gender'] = parse_gender_info(form)
	info['hometown'] = parse_hometown_info(form)
	info['interests'] = parse_interests_info(form)
	
	return info

