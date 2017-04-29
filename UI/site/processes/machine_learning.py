import numpy
from sklearn.neighbors import NearestNeighbors
import edit_dist
import sys

<<<<<<< HEAD
# function to match training set users to the target inputted and return the gifts that training set user specified
def target_match(training_data, target_info):
	# list of recommended gifts	
	target_gifts = []
	# loop through every interest of the target
	for interest in target_info['interests']:
		min_dist = sys.maxsize
		# for each interest, loop through every training set individual
		for i in range(len(training_data)):
			# for each training set individual, loop through each of that individual's interests
			for j in range(len(training_data[i]['interests'])):
				# Levenshtein distance between interest of training set individual & interest of target
				dist = edit_dist.editDistDP(interest, training_data[i]['interests'][j], len(interest), len(training_data[i]['interests'][j]))
				# if the distance is lower than any distance seen for this target interest, save it
				if dist < min_dist:
					min_dist = dist
					item = training_data[i]['gifts']
		# item now contains the gifts of the training set individual with the closest interest to this interest of the target
		# loop through each of these gifts
		for k in item:
			# check if this item was already added to the recommended gifts array through a previous iteration
			if k not in target_gifts:
				# add item to the list of recommended gifts for the target
				target_gifts.append(k)
	# target_gifts now contains all the gifts of the training set individuals with the closest interest to each of the interests of the target
=======
def target_match(training_data, target_info):
	target_gifts = []
	for interest in target_info['interests']:
		min_dist = sys.maxsize
		for i in range(len(training_data)):
			for j in range(len(training_data[i]['interests'])):
				dist = edit_dist.editDistDP(interest, training_data[i]['interests'][j], len(interest), len(training_data[i]['interests'][j]))
				if dist < min_dist:
					min_dist = dist
					item = training_data[i]['gifts']
		for k in item:
			if k not in target_gifts:
				target_gifts.append(k)	
>>>>>>> f30684c63fec3cad4934f223271f8dafc04fcfd5
	return target_gifts
