import database

database.connect_with_cred_file('db_creds.txt')
fb_key = database.get_key('fb_app_key')
print(fb_key)

