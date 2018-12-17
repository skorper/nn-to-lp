from nnlp import NeuralNetworkLP
from sklearn import datasets
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
import numpy as np
from timeit import default_timer as timer


# load and train
iris = datasets.load_iris()
X = iris.data
y = iris.target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
num_inputs = X.shape[1]
hidden_layers = (2, 2) #10, 10, 10 would be 3 layers of 10
model = MLPClassifier(activation='identity', hidden_layer_sizes=hidden_layers, max_iter=4000, random_state=1)
model.out_activation_ = "identity"
model.fit(X_train, y_train)
predictions = model.predict(X_test)
pred = model._predict(X_test)
error = (y_test != predictions).sum()
print ("Trained Neural Network with accuracy of " + str(100 - (error/len(predictions)))+".\n")
weights = np.array(model.coefs_)
bias = np.array(model.intercepts_)

temp_left_nodes = []
for m in range(len(X_test)):
	left_nodes = [(x) for x in X_test[m]]
	
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
		temp_left_nodes = []
	if left_nodes.index(max(left_nodes)) != predictions[m]:
		print ("diff= " + str(left_nodes) + " " + str(predictions[m]))
		error += 1

if error > 0:
	print ("Unable to confirm model.")
	exit()

accuracy = 0
threshold = 99
clingo_file = "tst.lp"
input_file = "input.lp"

nnlp = NeuralNetworkLP(weights, bias, clingo_file, input_file, _k = 4, _longest = 8, _threshold = threshold)
start = timer()
nnlp.generate()
accuracy = nnlp.test(X_test, y_test)
end = timer()

while accuracy < threshold:
	print ("Accuracy of " + str(accuracy) + " below threshold " + str(threshold) + ". Re-running with higher precision.")
	accuracy = 0
	nnlp.add_precision()
	start = timer()
	nnlp.generate()
	mid = timer()
	accuracy = nnlp.test(X_test, y_test)
	end = timer()

print ("Logic program generated.")
print ("Conversion Time: " + str(mid-start))
print ("Testing Time:    " + str(end-mid))
