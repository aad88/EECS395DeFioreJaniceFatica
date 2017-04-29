import numpy
from sklearn.neighbors import NearestNeighbors
import edit_dist
import sys

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
	return target_gifts
