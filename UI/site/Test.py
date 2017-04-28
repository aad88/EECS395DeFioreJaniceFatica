# native imports

# project imports
from processes import database

# external imports

database.connect_with_cred_file('db_creds.txt')
print(database.get_training_data())

