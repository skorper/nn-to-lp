from sklearn import datasets
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
import numpy as np
from scipy.special import expit as logistic_sigmoid

'''

confirm.py

This program replicates the functionality of the MLPRegressor with the identity activation function. I am 
doing this to ensure that I have a full understanding of the forward pass/prediction of the model.

'''

# load and train
iris = datasets.load_iris()
X = iris.data
y = iris.target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
num_inputs = X.shape[1]
hidden_layers = (2, 2) #10, 10, 10 would be 3 layers of 10
model = MLPClassifier(activation='identity', hidden_layer_sizes=hidden_layers, max_iter=4000, random_state=1)
model.out_activation_ = "identity"
print ("out: " + str(model.out_activation_))
model.fit(X_train, y_train)
predictions = model.predict(X_test)
error = (y_test != predictions).sum()
print ("Trained Neural Network with accuracy of " + str(100 - (error/len(predictions)))+".\n")
weights = np.array(model.coefs_)
bias = np.array(model.intercepts_)

print ("weights: " + str(weights))
print ("bias: " + str(bias))
print ("out: " + str(model.out_activation_))

print (predictions)

print ("Confirming forward pass of neural network...")
temp_left_nodes = []

scaler = 1
error = 0

print (predictions)

for m in range(len(X_test)):
	# left_nodes = X_test[i]
	left_nodes = [(x * scaler) for x in X_test[m]]
	
	#For each layer of weights
	for i in range(weights.shape[0]):
		for k in range (weights[i].shape[1]):
			sum = None
			# for each ROW of the matrix
			for j in range(weights[i].shape[0]):
				w = weights[i][j][k]
				l = left_nodes[j]
				mult = w * l
				if sum == None:
					sum = mult
				else:
					sum = sum + mult
			# add bias
			b = bias[i][k]
			sum = sum + b
			temp_left_nodes.append(sum)
			sum = None
		left_nodes = temp_left_nodes
		print (left_nodes)
		temp_left_nodes = []
	# print ("diff= " + str(left_nodes) + " " + str(predictions[m]))
	if left_nodes.index(max(left_nodes)) != predictions[m]:
		error += 1

print ("Error of " + str(error) + "/" + str(len(X_test)))