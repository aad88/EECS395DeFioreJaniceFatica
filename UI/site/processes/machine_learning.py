from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier(n_neighbors=2)
knn.fit(train_info['interests'], train['gifts'])
def target_match (target_info):
	target_gifts = knn.predict(target_info['interests'])
	return target_gifts