import sys
import pandas as pd
import numpy as np
from sklearn import datasets
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from rule_gen import RuleGenerator
import copy

'''
PREFIXES: 

	x: input layer
	w: weight
	h: hidden layer
	i: intermediate step in adder
	s: output bit of adder
	c: carry bit of adder

'''

'''
Return custom binary encoding, which shortens the resulting
number of bits.
'''
def convert_to_binary(num):
	is_negative = int(num < 0)
	num = abs(num)
	# print (num)
	num = num << 1
	# print (num)
	num = num + is_negative
	# print (num)
	# print (format(num, 'b'))
	return format(num, 'b')

iris = datasets.load_iris()

X = iris.data
y = iris.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

num_inputs = X.shape[1]
hidden_layers = (2, 2) #10, 10, 10 would be 3 layers of 10

model = MLPClassifier(activation='identity', hidden_layer_sizes=hidden_layers, max_iter=4000, random_state=1)
model.fit(X_train, y_train)

weights = np.array(model.coefs_)
scaler = 10
longest = 5#using 10 for now but will actually find longest later
weights_scaled = weights

print (weights)

weight_layers = []
weight_vars = [None] * weights_scaled.shape[0]

# Scale and convert weights
# & create weight variables for LP
for i in range(weights_scaled.shape[0]):
	weight_vars[i] = np.empty([weights_scaled[i].shape[0], weights_scaled[i].shape[1]], dtype=object)
	for j in range(weights_scaled[i].shape[0]):
		for k in range (weights_scaled[i].shape[1]):
			# Scale weight by scaler value
			weights_scaled[i][j][k] = int(weights_scaled[i][j][k] * scaler);
			# Convert weight to binary
			weights_scaled[i][j][k] = convert_to_binary(int(weights_scaled[i][j][k]))
			# Create weight var for LP
			weight_vars[i][j][k] = []
 			# Create weight vars for *each* bit
			for l in range(longest):
				weight_vars[i][j][k].append("w" + str(i) + str(j) + str(k) + str(l))
## Note: first I will generate the rules with unknown weights, 
## then I will replace the appropriate vars with the weight values
rule_gen = RuleGenerator(_verbose = False)

print(weights_scaled)


# Generate input layer variables (to be replaced with test data values!)
input = []
for i in range(num_inputs):
	input.append([])
	for j in range(longest):
		input[i].append("x" + str(i) + str(j))
print (input)

# generate rules for dot product of weights and inputs
num_hidden_layers = len(hidden_layers)

#holds the computed values for each node in the hidden layers

hidden_layers = []
left_nodes = input
temp_left_nodes = []

# TODO resolve 0 rules!
for i in range(weights_scaled.shape[0]):
	hidden_layers.append([])
	for k in range (weights_scaled[i].shape[1]):
		sum = None
		for j in range(weights_scaled[i].shape[0]):
			mult = rule_gen.multiply(weight_vars[i][j][k], left_nodes[j])
			if sum == None:
				sum = mult
			else:
				sum = rule_gen.add(sum, mult)
		# 	print ("\nMult: " + str(mult) + "\n")
		# print ("\nSum: " + str(sum) + "\n") 
		temp_left_nodes.append(sum)
		sum = None
	left_nodes = temp_left_nodes
	temp_left_nodes = []
	# print (str(weights_scaled[i][j][k]) + " * " + str(input[j]))
		
# todo print the variables input and output
# todo replace the values with the weights and associated rules
print ("Input variables: " + str(input) + "\n")
print ("Weight variables: " + str(weight_vars) + "\n")
print ("Final variables: " + str(left_nodes) + "\n")


# todo write to file (clingo syntactically correct)
rule_gen.print_rules()

# weights scaled now has the binary values! (with the first bit (on the right))
# being the signed bit. Now I need to convert the input value (X) to binary, 
# and do the dot product? But what exactly does that do? Don't I want a full
# LP of the trained NN without any information about the input?

'''

x1	h1  o1  |h1 = x1w11 + x2w12

x2  h2	o2	|


0000	0000	0000

0000	0000	0000



# Use activation function to create a non-ilnear mode

1. Get solver working DONE
2. Get multiplication working (for any num of bits) DONE
3. Combine into an empty LP DONE
4. Replace some vals with weights from this file (bits from weights)
5. Run through with test sample

'''