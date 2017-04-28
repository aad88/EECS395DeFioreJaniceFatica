# native imports

# project imports
import database, facebook, interests_form, amazon_search

# external imports


# -------------------------------
# SEARCH QUERY PROCESSING METHODS
# -------------------------------

def process_query(user_id, info):
	# grab the information pieces provided
	q_label = info['label']
	q_age = info['age']
	q_gender = info['gender']
	q_hometown = info['hometown']
	q_interests = info['interests']

	# create a record of this search query, if not anonymous
	search_id = None
	if user_id is not None:
		search_id = database.create_search(user_id, q_label)

	# TODO: MACHINE LEARNING IMPLEMENTATION HERE

	# TODO: AMAZON SEARCH IMPLEMENTATION HERE
	gift_ideas = []

	# enter each resulting gift idea into the database
	for idea in gift_ideas:
		# enter as new gift idea, if applicable
		#TODO

		# enter in connection to this search
		if search_id is not None:
			#TODO
			pass

# handle and process a search query coming from Facebook
def process_facebook_query(user_id, json):
	info = facebook.info_from_json(json)

	#process_query(user_id, info)

# handle and process a search query coming from the manual form
def process_manual_query(user_id, form):
	info = interests_form.info_from_form(form)

	process_query(user_id, info)
