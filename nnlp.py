import sys
import pandas as pd
import numpy as np
from sklearn import datasets
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from rule_gen import RuleGenerator
import copy
import subprocess
from subprocess import DEVNULL
from bitstring import BitArray
import math


class NeuralNetworkLP(object):
	def __init__(self, _weights, _bias, _clingo_file, _input_file, _k = 4, _longest = 8, _threshold = 100):
		self.threshold = _threshold
		self.clingo_file = _clingo_file
		self.input_file = _input_file
		self.weights = _weights
		self.bias = _bias
		self.k = _k
		self.longest = _longest
		self.rule_gen = RuleGenerator(_verbose = False, _k = self.k, _size = self.longest)

	def add_precision(self):
		self.k += 2
		self.longest = self.k * 2
		self.rule_gen = RuleGenerator(_verbose = False, _k = self.k, _size = self.longest)
		self.rule_gen.rules = []

		# Reset files
		open(self.clingo_file, 'w').close()
		open(self.input_file, 'w').close()

	def compute_longest(self):
		bits = []
		for i in range(self.weights.shape[0]):
			for k in range(self.weights[i].shape[1]):
				for j in range (self.weights[i].shape[0]):
					scaled = int(abs(self.weights[i][j][k]))
					if scaled == 0:
						bits.append(0)
						continue
					num_bits = math.ceil(math.log2(scaled))
					bits.append(num_bits)
		max_bits = max(bits)
		if max_bits == 1:
			return 4 + self.k
		return max_bits**2 + self.k

	def generate(self):
		print ("Running with " + str(self.longest - self.k) + "." + str(self.k) + " precision")
		self.process_weights()
		self.convert()
		self.save_weights()

	def generate_input_vars(self, num_input):
		input = []
		for i in range(num_input):
			input.append([])
			for j in range(self.longest):
				input[i].append("x" + str(i) + str(j))
		return input

	def process_weights(self):
		# print (self.weights)
		print ("Processing weights from neural network...")
		weights_scaled = copy.deepcopy(self.weights)
		weight_vars = [None] * weights_scaled.shape[0]

		# Scale and convert weights
		# & create weight variables for LP
		for i in range(weights_scaled.shape[0]):
			weight_vars[i] = np.empty([weights_scaled[i].shape[0], weights_scaled[i].shape[1]], dtype=object)
			for k in range(weights_scaled[i].shape[1]):
				for j in range (weights_scaled[i].shape[0]):
					# Convert weight to binary
					weights_scaled[i][j][k] = self.convert_to_binary(weights_scaled[i][j][k])
					# Create weight var for LP
					weight_vars[i][j][k] = []

		 			# Create weight vars for *each* bit
					for l in range(self.longest):
						weight_vars[i][j][k].append("w" + str(i) + str(j) + str(k) + str(l))

		self.weights_scaled = weights_scaled
		self.weight_vars = weight_vars

		print ("Processing bias from neural network... ")
		bias_scaled = copy.deepcopy(self.bias)
		bias_vars = [None] * len(bias_scaled)

		for i in range(len(bias_scaled)):
			bias_vars[i] = [None] * len(bias_scaled[i])
			for j in range(len(bias_scaled[i])):
				bias_scaled[i][j] = self.convert_to_binary(bias_scaled[i][j])
				bias_vars[i][j] = []
				for l in range(self.longest):
					bias_vars[i][j].append("b" + str(i) + str(j) + str(l))
		self.bias_scaled = bias_scaled
		self.bias_vars = bias_vars

	def convert(self):
		print ("Converting neural network to logic program...")
		hidden_layers = []
		left_nodes = self.generate_input_vars(self.weights[0].shape[0])
		temp_left_nodes = []
		k_vals = []

		#For each layer of weights
		for i in range(self.weights_scaled.shape[0]):
			hidden_layers.append([])

			# for each COLUMN of the matrix
			for k in range (self.weights_scaled[i].shape[1]):
				sum = None
				# for each ROW of the matrix
				for j in range(self.weights_scaled[i].shape[0]):
					mult = self.rule_gen.multiply(self.weight_vars[i][j][k], left_nodes[j])
					if sum == None:
						sum = mult
					else:
						sum = self.rule_gen.add(sum, mult)
				# add bias
				# print ("before adding bias: " + str(sum)) 
				sum = self.rule_gen.add(sum, self.bias_vars[i][k])
				# print ("after adding bias: " + str(sum))
				temp_left_nodes.append(sum)
				sum = None
			left_nodes = temp_left_nodes
			temp_left_nodes = []
		# print ("last nodes: " + str(left_nodes))
		self.output = left_nodes

	def save_weights(self):
		# Write rules to clingo file
		f = open(self.clingo_file,"w+")
		self.rule_gen.print_rules(f)
		# Add weights to clingo rules 
		for i in range(self.weights_scaled.shape[0]):
			for j in range(self.weights_scaled[i].shape[0]):
				for k in range (self.weights_scaled[i].shape[1]):
					scaled = str(int(self.weights_scaled[i][j][k]))
					weight = ("0" * (self.longest - len(scaled))) + scaled
					for l in range(len(weight)):
						if weight[l] == '1':
							f.write(self.weight_vars[i][j][k][l] + "." + "\n")

		# Add bias to clingo rules
		for i in range(len(self.bias_scaled)):
			for j in range(len(self.bias_scaled[i])):
				scaled = str(int(self.bias_scaled[i][j]))
				bias = ("0" * (self.longest - len(scaled))) + scaled
				for l in range(len(bias)):
					if bias[l] == '1':
						f.write(self.bias_vars[i][j][l] + "." + "\n")

		f.write("#show s.\n")
		f.close()


	def test(self, X_test, y_test):
		print ("Testing...")
		error = 0
		for i in range(len(X_test)):
			print ("\tTesting sample #" + str(i) + "...")
		# use the following values to add the the clingo program (add to file and pass as arg)
			f = open(self.input_file, "w+")
			# convert the arguments to binary
			# for each attribute in the sample
			for j in range(len(X_test[i])):
				attr = self.convert_to_binary(X_test[i][j])
				# for each bit in attribute
				for k in range(len(str(attr))):
					if str(attr)[k] == "1":
						bit_index = (self.longest - len(str(attr))) + k
						var_name = "x" + str(j) + str(bit_index)
						f.write(var_name + ".\n")
			f.close()
			# run Clingo program
			true_vars = self.run_clingo(self.clingo_file, [self.input_file])

			# Get result of clingo program
			results = []
			for node in self.output:
				binary_result = ""
				for var in node:
					if var in true_vars:
						binary_result = binary_result + "1"
					else:
						binary_result = binary_result + "0"

				results.append(float(self.convert_from_binary(binary_result)))
			# Find the largest from the results, which will give the class label
			LP_prediction = results.index(max(results))
			# compare the two. Are they the same? Record error, and if error > threshold redo with higher digits
			# print( "actual: " + str(y_test[i]) + " predicted: " + str(results) + " guessed(" + str(LP_prediction) + ")")
			if LP_prediction != y_test[i]:
				# print ("wrong")
				error += 1
		accuracy = 100 - error/len(X_test) * 100
		return accuracy


	'''
	2's complement + 1
	'''
	def sign(self, num):
		binary = ""
		for i in range(len(num)):
			if num[i] == "1":
				binary = binary + "0"
			elif num[i] == "0":
				binary = binary + "1"

		binary = int(binary, 2) + 1
		binary = str(bin(binary))
		binary = binary.replace("0b", "")
		return binary

	'''
	Convert to decimal binary with k points of precision after the decimal.
	'''
	def convert_to_binary(self, num):
		if self.k == 0:
			return np.binary_repr(num, width = self.longest)

		binary = ""
		is_negative = False
		if num < 0:
			is_negative = True

		integral = int(abs(num))
		fractional = abs(num) - abs(integral)
		integral = np.binary_repr(integral, width = self.longest - self.k)

		binary = str(integral)
		# binary += '.'
		k_count = self.k 
		while k_count > 0:
			k_count -= 1
			fractional *= 2
			fract_bit = int(fractional)
			if fract_bit == 1:
				fractional -= fract_bit
				binary += "1" 
			else:
				binary += "0"

		# print ("Binary before: " + binary)

		if is_negative:
			binary = self.sign(binary)

		for i in range ((self.longest) - len(binary)):
			binary = str("0") + str(binary)

		# print (binary)
		return str(binary)

	def convert_from_binary(self, num):
		# There will be k bits to the right of the decimal. 

		if self.k == 0:
			b = BitArray(bin=num)
			return b.int

		integral = num[:(self.longest - self.k)]
		integral = int(integral[1:], 2)
		integral = integral + int(num[0]) * (-1 * 2**(self.longest - self.k - 1))


		fractional = num[-self.k:]
		fr = 0

		for i in range (len(fractional)):
			fr = fr + (int(fractional[i]) * (1/2**(i+1)))

		binary = str(integral + fr)
		return binary

	def get_clingo_result(self, output):
		prev = ""
		for line in output:
			if "Answer" in prev:
				return line.split()
			prev = line
		return None

	def run_clingo(self, filename, args):
		try:
			clingo_output = subprocess.check_output(["clingo", filename, *args], stderr=DEVNULL)
			true_atoms = self.get_clingo_result(clingo_output)
		except subprocess.CalledProcessError as e:
			output = str(e.output)
			if "UNSATISFIABLE" in output:
				return "UNSATISFIABLE"
			finished = output.split("\\n")
			true_atoms = self.get_clingo_result(finished)
		return true_atoms

