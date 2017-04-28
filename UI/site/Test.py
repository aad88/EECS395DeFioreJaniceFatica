# native imports

# project imports
from processes import database, machine_learning

# external imports

database.connect_with_cred_file('db_creds.txt')
training_data = database.get_training_data()

machine_learning.train(training_data)

result = machine_learning.target_match({
	'interests': [
		'CWRU'
	]
})
print(result)

