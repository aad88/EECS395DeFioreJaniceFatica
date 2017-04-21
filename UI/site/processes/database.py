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
	session.execute(query)
	session.commit()
	#try:
	#	session.execute(query)
	#	session.commit()
	#except Exception:
	#	session.rollback()
	#	raise Exception

def select_query(query_template, session, *args):
	query = construct_query(query_template, *args)
	return session.execute(query).fetchall()

def hash_password(password):
	return hash(password)


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
	'{}',
	'{}',
	'{}',
	'{}'
)
;
"""

def create_user(username, password):
	password = hash_password(password)
	insert_query(CREATE_USER_QUERY, SESSION, username, password, datetime.datetime.now(), datetime.datetime.now())

USER_EXISTS_QUERY = """
SELECT
	count(u.username)
FROM
	users AS u
WHERE
	u.username = '{}'
;
"""

def user_exists(username):
	result = select_query(USER_EXISTS_QUERY, SESSION, username)
	
	result_int = int(result[0][0])
	return result_int is 1

LOGIN_QUERY = """
SELECT
	count(u.password)
FROM
	users AS u
WHERE
	u.username = '{}'
AND u.password = '{}'
;
"""

def is_valid_login(username, password):
	password = hash_password(password)
	result = select_query(LOGIN_QUERY, SESSION, username, password)
	
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
	'{}',
	'{}',
	'{}'
)
;
"""

def create_search(username, label):
	insert_query(CREATE_SEARCH_QUERY, SESSION, next_search_id(), username, label, datetime.datetime.now())

MOST_RECENT_SEARCH_QUERY = """
SELECT
	s.id, s.label, s.timestamp
FROM
	searches AS s
WHERE
	s.username = '{}'
AND s.timestamp = (
	SELECT
		max(s2.timestamp)
	FROM
		searches AS s2
	WHERE
		s2.username = '{}'
)
;
"""

def most_recent_search(username):
	result = select_query(MOST_RECENT_SEARCH_QUERY, SESSION, username, username)
	
	return result

# ---------------
# DATABASE TABLES
# ---------------

class Key(BASE):
	__tablename__ = 'keys'
	name = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
	key = sqlalchemy.Column(sqlalchemy.String, unique=False)

class User(BASE):
	__tablename__ = 'users'
	username = sqlalchemy.Column(sqlalchemy.String, primary_key=True, unique=True)
	password = sqlalchemy.Column(sqlalchemy.String, nullable=False)
	created = sqlalchemy.Column(sqlalchemy.DateTime)
	last_login = sqlalchemy.Column(sqlalchemy.DateTime)

class Search(BASE):
	__tablename__ = 'searches'
	id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
	username = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey('users.username'), nullable=False)
	label = sqlalchemy.Column(sqlalchemy.String, nullable=False)
	timestamp = sqlalchemy.Column(sqlalchemy.DateTime)

class SearchIdea(BASE):
	__tablename__ = 'search_ideas'
	id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('searches.id'), primary_key=True)
	name = sqlalchemy.Column(sqlalchemy.String, primary_key=True)

