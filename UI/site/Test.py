from processes import database

database.connect_with_cred_file('db_creds.txt')
print(database.get_key('fb_app_secret'))

