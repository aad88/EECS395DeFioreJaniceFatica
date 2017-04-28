# native imports

# project imports
import database, facebook, interests_form, machine_learning, amazon_search

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
	
	# get a final list of keywords to search from machine learning prediction of interests
	#search_interests = machine_learning.target_match(q_interests)
	search_interests = q_interests
	
	# search on the interests via Amazon
	gift_ideas = []
	for search_interest in search_interests:
		result = amazon_search.searchByKeyword(search_interest)
		for idea in result:
			if idea not in gift_ideas:
				gift_ideas.append(idea)
	
	# enter each resulting gift idea into the database
	for idea in gift_ideas:
		# enter as new gift idea, if applicable
		if database.get_idea(idea['id']) is None:
			database.create_idea(idea['id'], idea['name'], url=idea['url'], price=idea['price'], image_url=idea['imageurl'], image_width=idea['imagewidth'], image_height=idea['imageheight'])
	
		# enter in connection to this search
		if search_id is not None:
			database.create_search_idea(search_id, idea['id'])

# handle and process a search query coming from Facebook
def process_facebook_query(user_id, json):
	info = facebook.info_from_json(json)

	#process_query(user_id, info)

# handle and process a search query coming from the manual form
def process_manual_query(user_id, form):
	info = interests_form.info_from_form(form)

	process_query(user_id, info)
