from nnlp import NeuralNetworkLP
from sklearn import datasets
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
import numpy as np

# load and train
iris = datasets.load_iris()
X = iris.data
y = iris.target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
num_inputs = X.shape[1]
hidden_layers = (2, 2) #10, 10, 10 would be 3 layers of 10
model = MLPClassifier(activation='identity', hidden_layer_sizes=hidden_layers, max_iter=4000, random_state=1)
model.fit(X_train, y_train)
predictions = model.predict(X_test)
error = (y_test != predictions).sum()
print ("Trained Neural Network with accuracy of " + str(100 - (error/len(predictions)))+".\n")
weights = np.array(model.coefs_)
bias = np.array(model.intercepts_)
print ("bias: " + str(bias))


accuracy = 0
threshold = 99
clingo_file = "tst.lp"
input_file = "input.lp"

nnlp = NeuralNetworkLP(weights, bias, clingo_file, input_file, _threshold = threshold)

while accuracy < threshold:
	nnlp.add_precision()
	nnlp.generate()
	accuracy = nnlp.test(X_test, y_test)
	print ("Accuracy of " + str(accuracy) + " below threshold " + str(threshold) + ". Re-running with higher precision.")
	accuracy = 0