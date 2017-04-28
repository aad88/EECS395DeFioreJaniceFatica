import numpy
from sklearn.neighbors import NearestNeighbors
import editdistance

knn = NearestNeighbors(n_neighbors = 1, 
		      algorithm = 'auto',
		      metric = lambda a,b: editdistance.eval(a, b))

def train(training_data):
	interests = numpy.reshape(training_data[0]['interests'], (1, -1))
	print(interests)
	gifts = numpy.reshape(training_data[0]['gifts'], (1, -1))
	print(gifts)
	knn.fit(interests, gifts)

def target_match(target_info):
	target_gifts = knn.predict(1.0)
	return target_gifts

