# native imports
import sys

# project imports
import cred_file

# external imports
try:
	import sqlalchemy
	import sqlalchemy.ext.declarative
except ImportError:
	print("IMPORT ERROR: Need to install Flask via pip")
	sys.exit(1)

KEY_QUERY = """
SELECT
	keys.key
FROM
	keys
WHERE
	keys.name = '{}'
;
"""

BASE = sqlalchemy.ext.declarative.declarative_base()
SESSION = sqlalchemy.orm.scoped_session(sqlalchemy.orm.sessionmaker())

def init_db(username, password, database):
	connection_url = sqlalchemy.engine.url.make_url('postgresql://localhost/')
	connection_url.username = username
	connection_url.password = password
	connection_url.database = database
	engine = sqlalchemy.create_engine(connection_url)
	SESSION.remove()
	SESSION.configure(bind=engine)
	BASE.metadata.create_all(engine)

def connect(username, password, database):
	init_db(username, password, database)
	return SESSION

def connect_with_cred_file(file_path):
	creds = cred_file.read(file_path)
	return connect(creds['username'], creds['password'], creds['database'])

# TODO: Sanitize query args to defend against injection
def sanitize(val):
	return val

def run_query(query, session=SESSION):
	return session.execute(query).fetchall()

def get_key(name, session=SESSION):
	name = sanitize(name)
	
	query = KEY_QUERY.format(name)
	result = run_query(query, session=session)
	return result[0][0]

class Key(BASE):
	__tablename__ = 'keys'
	name = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
	key = sqlalchemy.Column(sqlalchemy.String, unique=False)

