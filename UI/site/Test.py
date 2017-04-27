from processes import database

database.connect_with_cred_file('db_creds.txt')
#database.create_search('Zanice', 'Older')
#database.create_search('Zanice', 'Newer')
print(database.get_idea('14'))

