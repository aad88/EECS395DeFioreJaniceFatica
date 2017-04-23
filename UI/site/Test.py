from processes import database

database.connect_with_cred_file('db_creds.txt')
#database.create_search('Zanice', 'Older')
#database.create_search('Zanice', 'Newer')
database.get_search(3)
print(database.get_searches_for_user('Zanice'))

