# native imports
import csv

# project imports
from processes import database

# external imports


TRAINING_DATA_SRC = 'data/training_data.csv'
TRAINING_DATA_DELIM = ','

TD_NAME_INDEX = 0
TD_IDEA_1_INDEX = 2
TD_IDEA_2_INDEX = 3
TD_IDEA_3_INDEX = 4

with open(TRAINING_DATA_SRC) as training_data:
	reader = csv.reader(training_data, delimiter=TRAINING_DATA_DELIM)
	
	for row in reader:
		name = row[TD_NAME_INDEX]
		idea_1 = row[TD_IDEA_1_INDEX]
		idea_2 = row[TD_IDEA_2_INDEX]
		idea_3 = row[TD_IDEA_3_INDEX]
		
		print "<name={}> [{}, {}, {}]".format(name, idea_1, idea_2, idea_3)

