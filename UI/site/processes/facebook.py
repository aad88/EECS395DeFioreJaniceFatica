# native imports
import string
import word_frequency

# project imports

# external imports


# ---------------------------
# PRUNING, CLEANING VARIABLES
# ---------------------------

# keyword to trigger parsing of story information
SHARED_KEYWORD = ' shared '
# keywords at the end of a story to suggest reference to an interest
SHARED_ITEM_KEYWORDS = [
	'\'s photo.',
	'\'s video.'
]

# whitespace to remove from messages
WHITESPACE_TO_REMOVE = string.whitespace.replace('\n', '').replace(' ', '')

# -------------------------
# PRUNING, CLEANING METHODS
# -------------------------

# clean up unacceptable characters in a string
def sanitize(string):
	ascii_string = ''
	for char in string:
		if 0 < ord(char) <= 255:
			ascii_string += char
	return str(ascii_string)

# returns a possible interest if the story suggests one, or None otherwise
def prune_story(name, story):
	if story is None:
		return story

	# clean the story
	story = sanitize(story)

	# start to an important story: "YOUR_NAME shared "
	shared_story_start = name + SHARED_KEYWORD

	# prune based on the keyword ' shared '
	if story.startswith(shared_story_start):
		# grab the details of what was shared
		shared_item = story[len(shared_story_start):]

		# if the story references another page, take the page title as an interest
		for item_keyword in SHARED_ITEM_KEYWORDS:
			if shared_item.endswith(item_keyword):
				shared_item = shared_item[:-len(item_keyword)]

				# some cases involve an extraneous backslash, I don't know why
				if shared_item[-1] == '\\':
					shared_item = shared_item[:-1]

				return shared_item

	return None

# returns the (clean) text of a message, along with a separate list of removed hashtags
def prune_message(message):
	if message is None:
		return None

	# clean the message
	message = sanitize(message)
	message = message.strip(WHITESPACE_TO_REMOVE)
	message = message.replace('\n', ' ')
	message = message.replace('\\n', ' ')

	# remove hashtags that exist in the message, separating them for future use
	index = 0
	left_index = -1
	hashtags = []
	while index < len(message):
		# iterating over each character, identify hashtag beginnings/endings and use them to pull out the hashtag
		current_char = message[index]
		if left_index is -1:
			if current_char == '#':
				# hashtag has begun
				left_index = index
		else:
			current_char_code = ord(current_char)
			is_number = 48 <= current_char_code <= 57
			is_lc_letter = 97 <= current_char_code <=122
			is_uc_letter = 65 <= current_char_code <= 90
			if not (is_number or is_lc_letter or is_uc_letter):
				# hashtag has ended
				hashtag = message[left_index + 1:index]
				message = message[:left_index] + message[index:]
				hashtags.append(hashtag)
				index = left_index
				left_index = -1

		index += 1
	# if a hashtag is occupying the last characters of a message, complete the removal
	if left_index is not -1:
		hashtag = message[left_index + 1:]
		message = message[:left_index]
		hashtags.append(hashtag)

	return (message, hashtags)

# separate post objects into stories, messages, and hashtags
# stories and hashtags suggest possible interests, messages are to be analyzed further
def digest_posts(name, posts):
	stories = []
	messages = []
	hashtags = []

	for post in posts:
		# process the provided information
		current_story = prune_story(name, post['story'])
		current_message = prune_message(post['message'])

		# separate the results into their respective categories
		if current_story is not None:
			stories.append(current_story)
		if current_message is not None:
			messages.append(current_message[0])
			for hashtag in current_message[1]:
				hashtags.append(hashtag)

	# construct the resulting dictionary
	digested_posts = {}
	digested_posts['stories'] = stories
	digested_posts['messages'] = messages
	digested_posts['hashtags'] = hashtags

	return digested_posts

# process the information available from Facebook's returned JSON of a target
def info_from_json(json):
	# take the basic information available
	name = str(json['name'])

	# separate out, analyze posts for possible interests
	digested_posts = digest_posts(name, json['posts'])
	
	# word frequency processing of messages for more interests
	interests = []
	frequent_words = word_frequency.get_most_frequent_words(digested_posts['messages'])
	for word in frequent_words:
		interests.append(word)

	# compile a final list of interests
	for story in digested_posts['stories']:
		interests.append(story)
	for hashtag in digested_posts['hashtags']:
		interests.append(hashtag)

	# construct the resulting dictionary
	info = {}
	info['label'] = json['name']
	info['age'] = None
	info['gender'] = None
	info['hometown'] = None
	info['interests'] = interests

	return info
