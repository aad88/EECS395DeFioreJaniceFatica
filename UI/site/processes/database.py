# native imports
import datetime
import sys

# project imports
import db_cred_file

# external imports
try:
	import sqlalchemy
	import sqlalchemy.ext.declarative
except ImportError:
	print("IMPORT ERROR: Need to install SQLAlchemy")
	sys.exit(1)

# ------------------
# CONNECTION GLOBALS
# ------------------

URL_BASE = "{}://{}/"
DEF_SERVICE = 'postgresql'
DEF_ADDRESS = 'localhost'

# --------------------
# CONNECTION PROCESSES
# --------------------

BASE = sqlalchemy.ext.declarative.declarative_base()
SESSION = sqlalchemy.orm.scoped_session(sqlalchemy.orm.sessionmaker())

def init_db(username, password, database, service=DEF_SERVICE, address=DEF_ADDRESS):
	url = URL_BASE.format(service, address)
	connection_url = sqlalchemy.engine.url.make_url(url)
	connection_url.username = username
	connection_url.password = password
	connection_url.database = database
	engine = sqlalchemy.create_engine(connection_url)
	SESSION.remove()
	SESSION.configure(bind=engine)
	BASE.metadata.create_all(engine)

def connect(username, password, database, service=DEF_SERVICE, address=DEF_ADDRESS):
	init_db(username, password, database, service=service, address=address)
	return SESSION

def connect_with_cred_file(file_path):
	creds = db_cred_file.read(file_path)
	return connect(
		creds['username'],
		creds['password'],
		creds['database'],
		service=creds['service'],
		address=creds['address']
	)

def clear_database():
	engine = SESSION.get_bind()
	BASE.metadata.drop_all(bind=engine)
	BASE.metadata.create_all(bind=engine)

def construct_query(template, *args):
	return template.format(*args)

def insert_query(query_template, session, *args):
	query = construct_query(query_template, *args)
	try:
		session.execute(query)
		session.commit()
	except Exception:
		session.rollback()
		raise Exception

def select_query(query_template, session, *args):
	query = construct_query(query_template, *args)
	return session.execute(query).fetchall()


# -------------------------------
# QUERIES - GET / UPDATE KEY INFO
# -------------------------------

KEY_QUERY = """
SELECT
	k.key
FROM
	keys AS k
WHERE
	k.name = '{}'
;
"""

def get_key(name):
	result = select_query(KEY_QUERY, SESSION, name)
	
	return result[0][0]

# -------------------------
# QUERIES - USER PROCEDURES
# -------------------------

CREATE_USER_QUERY = """
INSERT INTO
	users
VALUES (
	{},
	'{}',
	'{}'
)
;
"""

def create_user(id, name, token):
	insert_query(CREATE_USER_QUERY, SESSION, username, password, datetime.datetime.now(), datetime.datetime.now())

USER_EXISTS_QUERY = """
SELECT
	count(u.id)
FROM
	users AS u
WHERE
	u.id = {}
;
"""

def user_exists(id):
	result = select_query(USER_EXISTS_QUERY, SESSION, id)
	
	result_int = int(result[0][0])
	return result_int is 1

# ------------------
# QUERIES - SEARCHES
# ------------------

NEXT_SEARCH_ID_QUERY = """
SELECT
	max(s.id)
FROM
	searches AS s
;
"""

def next_search_id():
	result = select_query(NEXT_SEARCH_ID_QUERY, SESSION)
	result = result[0][0]
	
	result_int = 0 if result is None else int(result)
	return result_int + 1

CREATE_SEARCH_QUERY = """
INSERT INTO
	searches
VALUES (
	{},
	{},
	'{}',
	'{}'
)
;
"""

def create_search(user_id, label):
	search_id = next_search_id()
	insert_query(CREATE_SEARCH_QUERY, SESSION, search_id, user_id, label, datetime.datetime.now())
	
	return search_id

CREATE_SEARCH_IDEA_QUERY = """
INSERT INTO
	search_ideas
VALUES (
	{},
	'{}'
)
;
"""

def create_search_idea(search_id, name):
	insert_query(CREATE_SEARCH_IDEA_QUERY, SESSION, search_id, name)

SEARCH_IDEAS_QUERY = """
SELECT
	si.idea_id
FROM
	search_ideas AS si
WHERE
	si.search_id = {}
;
"""

def get_search_ideas(id):
	result = select_query(SEARCH_IDEAS_QUERY, SESSION, id)
	if len(result) is 0:
		return None
	
	ideas = []
	for item in result:
		ideas.append(item[0])
	
	return ideas

SEARCH_QUERY = """
SELECT
	s.user, s.label, s.timestamp
FROM
	searches AS s
WHERE
	s.id = {}
;
"""

def get_search(id):
	result = select_query(SEARCH_QUERY, SESSION, id)
	if len(result) is 0:
		return None
	result = result[0]
	
	search = {}
	search['id'] = id
	search['user'] = result[0]
	search['label'] = result[1]
	search['timestamp'] = result[2]
	search['ideas'] = get_search_ideas(id)
	
	return search

MOST_RECENT_USER_SEARCH_QUERY = """
SELECT
	s.id, s.label, s.timestamp
FROM
	searches AS s
WHERE
	s.user = {}
AND s.timestamp = (
	SELECT
		max(s2.timestamp)
	FROM
		searches AS s2
	WHERE
		s2.user = {}
)
;
"""

def get_most_recent_search(user_id):
	result = select_query(MOST_RECENT_USER_SEARCH_QUERY, SESSION, user_id, user_id)
	if len(result) is 0:
		return None
	result = result[0]
	
	search = {}
	search['id'] = result[0]
	search['user'] = user_id
	search['label'] = result[1]
	search['timestamp'] = result[2]
	search['ideas'] = get_search_ideas(result[0])
	
	return search

SEARCH_IDEAS_FOR_USER_QUERY = """
SELECT
	si.search_id, s.label, si.idea_id
FROM (
		search_ideas AS si
	JOIN
		searches AS s
	ON
		si.search_id = s.id
)
WHERE
	s.user = {}
;
"""

def get_search_ideas_for_user(user_id):
	result = select_query(SEARCH_IDEAS_FOR_USER_QUERY, SESSION, user_id)
	if len(result) is 0:
		return None
	
	ideas = []
	for item in result:
		idea = {}
		idea['search_id'] = item[0]
		idea['search_label'] = item[1]
		idea['idea_id'] = item[2]
		
		ideas.append(idea)
	
	return ideas

SEARCHES_FOR_USER_QUERY = """
SELECT
	s.id, s.label, s.timestamp
FROM
	searches AS s
WHERE
	s.user = {}
ORDER BY s.timestamp DESC
;
"""

def get_searches_for_user(user_id):
	result = select_query(SEARCHES_FOR_USER_QUERY, SESSION, user_id)
	if len(result) is 0:
		return None
	
	ideas = get_search_ideas_for_user(user_id)
	
	searches = []
	for item in result:
		search = {}
		search['id'] = item[0]
		search['user'] = user_id
		search['label'] = item[1]
		search['timestamp'] = item[2]
		
		search_ideas = []
		current_search_id = search['id']
		for idea in ideas:
			if idea['search_id'] is current_search_id:
				search_ideas.append(idea['idea_id'])
		search['ideas'] = search_ideas
		
		searches.append(search)
	
	return searches

# ---------------
# DATABASE TABLES
# ---------------

class Key(BASE):
	__tablename__ = 'keys'
	name = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
	key = sqlalchemy.Column(sqlalchemy.String, unique=False)

class User(BASE):
	__tablename__ = 'users'
	id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
	name = sqlalchemy.Column(sqlalchemy.String)
	token = sqlalchemy.Column(sqlalchemy.Text)

class Idea(BASE):
	__tablename__ = 'ideas'
	id = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
	name = sqlalchemy.Column(sqlalchemy.String)
	url = sqlalchemy.Column(sqlalchemy.String)
	price = sqlalchemy.Column(sqlalchemy.String)
	image_url = sqlalchemy.Column(sqlalchemy.String)
	image_width = sqlalchemy.Column(sqlalchemy.Integer)
	image_height = sqlalchemy.Column(sqlalchemy.Integer)

class Search(BASE):
	__tablename__ = 'searches'
	id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
	user = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), nullable=False)
	label = sqlalchemy.Column(sqlalchemy.String, nullable=False)
	timestamp = sqlalchemy.Column(sqlalchemy.DateTime)

class SearchIdea(BASE):
	__tablename__ = 'search_ideas'
	search_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('searches.id'), primary_key=True)
	idea_id = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey('ideas.id'), primary_key=True)

