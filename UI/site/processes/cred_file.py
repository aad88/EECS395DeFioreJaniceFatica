# native imports
import string
import sys

# project imports

# external imports

WHITESPACE_TO_REMOVE = string.whitespace.replace(' ', '')

CRED_DELIM = '='
ACCEPTED_CREDS = [
	'username',
	'password',
	'database'
]

def read(file_path):
	cred_dict = {}
	
	with open(file_path) as file_contents:
		for line in file_contents:
			cred = line.strip(WHITESPACE_TO_REMOVE)
			split_cred = cred.split(CRED_DELIM)
			
			if split_cred[0] not in ACCEPTED_CREDS or len(split_cred) is not 2:
				raise Exception
			
			cred_dict[split_cred[0]] = split_cred[1]
	
	return cred_dict

