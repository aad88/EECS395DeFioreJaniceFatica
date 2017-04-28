# native imports
import csv

# project imports
from processes import database

# external imports


TRAINING_DATA_SRC = 'training_set/training_data.csv'
TRAINING_DATA_DELIM = ','

TD_NAME_INDEX = 0
TD_GIFT_1_INDEX = 2
TD_GIFT_2_INDEX = 3
TD_GIFT_3_INDEX = 4
TD_INTEREST_1_INDEX = 10
TD_INTEREST_2_INDEX = 11
TD_INTEREST_3_INDEX = 12

database.connect_with_cred_file('db_creds.txt')
with open(TRAINING_DATA_SRC) as training_data:
	reader = csv.reader(training_data, delimiter=TRAINING_DATA_DELIM)
	
	for row_num, row in enumerate(reader):
		if row_num is 0:
			continue
		
		name = row[TD_NAME_INDEX]
		interest_1 = row[TD_INTEREST_1_INDEX]
		interest_2 = row[TD_INTEREST_2_INDEX]
		interest_3 = row[TD_INTEREST_3_INDEX]
		gift_1 = row[TD_GIFT_1_INDEX]
		gift_2 = row[TD_GIFT_2_INDEX]
		gift_3 = row[TD_GIFT_3_INDEX]
		
		print "<name={}> [{}, {}, {}] => [{}, {}, {}]".format(name, interest_1, interest_2, interest_3, gift_1, gift_2, gift_3)
		
		interests = []
		if interest_1 is not None and interest_1 != '':
			interests.append(interest_1)
		if interest_2 is not None and interest_2 != '':
			interests.append(interest_2)
		if interest_3 is not None and interest_3 != '':
			interests.append(interest_3)
		
		gifts = []
		if gift_1 is not None and gift_1 != '':
			gifts.append(gift_1)
		if gift_2 is not None and gift_2 != '':
			gifts.append(gift_2)
		if gift_3 is not None and gift_3 != '':
			gifts.append(gift_3)
		
		database.create_training_set(interests, gifts)

