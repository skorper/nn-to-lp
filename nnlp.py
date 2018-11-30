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
from bitstring import Bits
import math


class NeuralNetworkLP(object):
	def __init__(self, _weights, _bias, _clingo_file, _input_file, _threshold = 100):
		self.threshold = _threshold
		self.clingo_file = _clingo_file
		self.input_file = _input_file
		self.weights = _weights
		self.bias = _bias
		self.scaler = 1
		self.longest = 4
		self.rule_gen = RuleGenerator(_verbose = False, _size = self.longest)

	def add_precision(self):
		self.scaler *= 10
		self.longest += 4
		print ("Running with " + str(self.longest) + " precision")
		self.rule_gen = RuleGenerator(_verbose = False, _size = self.longest)

	def generate(self):
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
		print ("Processing weights from neural network...")
		weights_scaled = copy.deepcopy(self.weights)
		weight_vars = [None] * weights_scaled.shape[0]

		# Scale and convert weights
		# & create weight variables for LP
		for i in range(weights_scaled.shape[0]):
			weight_vars[i] = np.empty([weights_scaled[i].shape[0], weights_scaled[i].shape[1]], dtype=object)
			for k in range(weights_scaled[i].shape[1]):
				for j in range (weights_scaled[i].shape[0]):
					# Scale weight by scaler value
					weights_scaled[i][j][k] = int(weights_scaled[i][j][k] * self.scaler);
					# Convert weight to binary
					weights_scaled[i][j][k] = self.convert_to_binary(int(weights_scaled[i][j][k]), self.longest)
					# Create weight var for LP
					weight_vars[i][j][k] = []
		 			# Create weight vars for *each* bit
					for l in range(self.longest):
						weight_vars[i][j][k].append("w" + str(i) + str(j) + str(k) + str(l))
		self.weights_scaled = weights_scaled
		self.weight_vars = weight_vars
		# print (self.weight_vars)

	def convert(self):
		print ("Converting neural network to logic program...")
		hidden_layers = []
		left_nodes = self.generate_input_vars(self.weights[0].shape[0])
		temp_left_nodes = []

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
				temp_left_nodes.append(sum)
				sum = None
			left_nodes = temp_left_nodes
			temp_left_nodes = []
		self.output = left_nodes

	def save_weights(self):
		# Write rules to clingo file
		f = open(self.clingo_file,"w+")
		self.rule_gen.print_rules(f)

		# print (self.weights_scaled)

		# Add weights to clingo rules 
		# todo combine with above looping as to not repeat work
		for i in range(self.weights_scaled.shape[0]):
			for j in range(self.weights_scaled[i].shape[0]):
				for k in range (self.weights_scaled[i].shape[1]):
					scaled = str(int(self.weights_scaled[i][j][k]))
					weight = ("0" * (self.longest - len(scaled))) + scaled
					# print ('weight: ' + weight + " " + str(self.weight_vars[i][j][k]))
					for l in range(len(weight)):
						if weight[l] == '1':
							f.write(self.weight_vars[i][j][k][l] + "." + "\n")
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
				attr = int(X_test[i][j]) # do I need to * by scaler?
				attr = self.convert_to_binary(attr, self.longest)
				# for each bit in attribute
				for k in range(len(str(attr))):
					if str(attr)[k] == "1":
						bit_index = (self.longest - len(str(attr))) + k
						var_name = "x" + str(j) + str(bit_index)
						f.write(var_name + ".\n")
			f.close()
			# run Clingo program
			true_vars = self.run_clingo(self.clingo_file, [self.input_file])
			# print (true_vars)

			# Get result of clingo program
			results = []
			for node in self.output:
				binary_result = ""
				for var in node:
					if var in true_vars:
						binary_result = binary_result + "1"
					else:
						binary_result = binary_result + "0"

				results.append(self.convert_from_binary(binary_result))
			# Find the largest from the results, which will give the class label
			LP_prediction = results.index(max(results))
			# compare the two. Are they the same? Record error, and if error > threshold redo with higher digits
			if LP_prediction != y_test[i]:
				error += 1
		accuracy = 100 - error/len(X_test) * 100
		return accuracy

	def convert_to_binary(self, num, digits):
		bin = np.binary_repr(num, width = digits)
		# print (digits)
		# print (str(num) + " --> " + bin)
		return bin

	def convert_from_binary(self, num):
		n = Bits(bin=num)
		return n.int

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