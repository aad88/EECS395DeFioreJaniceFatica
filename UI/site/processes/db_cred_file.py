# native imports
import string
import sys

# project imports

# external imports


# ----------------------
# FILE PARSING VARIABLES
# ----------------------

# whitespace to remove from each line of the read file
WHITESPACE_TO_REMOVE = string.whitespace.replace(' ', '')

# delimiter for credential entries
CRED_DELIM = '='
# list of accepted credential entries
ACCEPTED_CREDS = [
	'service',
	'address',
	'username',
	'password',
	'database'
]

# -------------------
# FILE PARSING METHOD
# -------------------

# parse the given file for database credentials
def read(file_path):
	cred_dict = {}
	
	with open(file_path) as file_contents:
		for line in file_contents:
			# clean the line
			cred = line.strip(WHITESPACE_TO_REMOVE)
			split_cred = cred.split(CRED_DELIM)
			
			# credential must be an accepted entry and must have a value
			if split_cred[0] not in ACCEPTED_CREDS or len(split_cred) is not 2:
				raise Exception
			
			# add the parsed credential
			cred_dict[split_cred[0]] = split_cred[1]
	
	return cred_dict

