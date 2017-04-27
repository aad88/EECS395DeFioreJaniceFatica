# native imports

# project imports

# external imports


SHARED_KEYWORD = ' shared '

SHARED_ITEM_KEYWORDS = [
	'\'s photo.',
	'\'s video.'
]

def prune_story(name, story):
	if story is None:
		return story
	
	shared_story_start = name + SHARED_KEYWORD
	
	# prune based on the keyword ' shared '
	if story.startswith(shared_story_start):
		shared_item = story[len(shared_story_start):]
		
		for item_keyword in SHARED_ITEM_KEYWORDS:
			if shared_item.endswith(item_keyword):
				shared_item = shared_item[:-len(item_keyword)]
				
				if shared_item[-1] == '\\':
					shared_item = shared_item[:-1]
				
				return shared_item
	
	return None

def sanitize_message(message):
	if message is None:
		return message
	
	# TODO: sanitize of annoying-ass emoji characters
	
	return message

def digest_posts(name, posts):
	stories = []
	messages = []
	
	for post in posts:
		current_story = prune_story(name, post['story'])
		current_message = sanitize_message(post['message'])
		
		if current_story is not None:
			stories.append(current_story)
		if current_message is not None:
			messages.append(current_message)
	
	digested_posts = {}
	digested_posts['stories'] = stories
	digested_posts['messages'] = messages
	
	return digested_posts

def info_from_json(json):
	name = str(json['name'])
	
	digested_posts = digest_posts(name, json['posts'])
	print(digested_posts['stories'])
	
	info = {}
	
	info['label'] = json['name']
	info['age'] = None
	info['gender'] = None
	info['hometown'] = None
	info['interests'] = None
	
	return info
