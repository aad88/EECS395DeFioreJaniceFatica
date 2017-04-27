# native imports
import string

# project imports

# external imports


SHARED_KEYWORD = ' shared '
SHARED_ITEM_KEYWORDS = [
	'\'s photo.',
	'\'s video.'
]

WHITESPACE_TO_REMOVE = string.whitespace.replace('\n', '').replace(' ', '')

def sanitize(string):
	ascii_string = ''
	for char in string:
		if 0 < ord(char) <= 255:
			ascii_string += char
	return str(ascii_string)

def prune_story(name, story):
	if story is None:
		return story
	
	story = sanitize(story)
	
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

def prune_message(message):
	if message is None:
		return None
	
	message = sanitize(message)
	
	message = message.strip(WHITESPACE_TO_REMOVE)
	message = message.replace('\n', ' ')
	message = message.replace('\\n', ' ')
	
	index = 0
	left_index = -1
	hashtags = []
	while index < len(message):
		current_char = message[index]
		if left_index is -1:
			if current_char == '#':
				left_index = index
		else:
			current_char_code = ord(current_char)
			is_number = 48 <= current_char_code <= 57
			is_lc_letter = 97 <= current_char_code <=122
			is_uc_letter = 65 <= current_char_code <= 90
			if not (is_number or is_lc_letter or is_uc_letter):
				hashtag = message[left_index + 1:index]
				message = message[:left_index] + message[index:]
				hashtags.append(hashtag)
				index = left_index
				left_index = -1
		
		index += 1
	if left_index is not -1:
		hashtag = message[left_index + 1:]
		message = message[:left_index]
		hashtags.append(hashtag)
	
	return (message, hashtags)

def digest_posts(name, posts):
	stories = []
	messages = []
	hashtags = []
	
	for post in posts:
		current_story = prune_story(name, post['story'])
		current_message = prune_message(post['message'])
		
		if current_story is not None:
			stories.append(current_story)
		if current_message is not None:
			messages.append(current_message[0])
			for hashtag in current_message[1]:
				hashtags.append(hashtag)
	
	digested_posts = {}
	digested_posts['stories'] = stories
	digested_posts['messages'] = messages
	digested_posts['hashtags'] = hashtags
	
	return digested_posts

def info_from_json(json):
	name = str(json['name'])
	
	digested_posts = digest_posts(name, json['posts'])
	#print("STORIES: {}".format(digested_posts['stories']))
	#print("HASHTAGS: {}".format(digested_posts['hashtags']))
	#print("MESSAGES: {}".format(digested_posts['messages']))
	
	# TODO: word frequency processing of messages for more interests
	
	interests = []
	for story in digested_posts['stories']:
		interests.append(story)
	for hashtag in digested_posts['hashtags']:
		interests.append(hashtags)
	
	info = {}
	
	info['label'] = json['name']
	info['age'] = None
	info['gender'] = None
	info['hometown'] = None
	info['interests'] = interests
	
	return info
