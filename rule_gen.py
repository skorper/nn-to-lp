from operator import xor
import collections

class RuleGenerator(object):

	def __init__(self, _size = 4, _rules = [], _var_id = 0, _verbose = False):
		self.rules = _rules
		self.var_id = _var_id
		self.verbose = _verbose
		self.size = _size

	#####################
	#					#
	# 'Public' Methods: #
	#                   #
	#####################

	def add(self, num1, num2):
		return self._add(num1, num2)[1:]

	def _add(self, num1, num2):
		self.print_if ("adding " + str(num1) + " and " + str(num2))
		num1, num2 = self.__resolve_lengths(num1, num2)
		# num1, num2 = same_length(num1, num2)
		# sum holds the vars which the result was placed into (for next comp)
		sum = [None] * int(len(max(num1, num2)) + 1)
		c = "z"
		for i in range(len(num1) - 1, -1, -1):
			s, c = self.__full_adder(str(num1[i]), str(num2[i]), c)
			sum[i+1] = s
		sum[0] = c
		# print ("sum: " + str(sum))
		return sum

	def multiply(self, num1, num2):
		self.print_if ("Multiplying " + str(num1) + " and " + str(num2))
		shift_index = 0
		sum = ["z"] * len(num2)
		for bit_2, i in zip(reversed(num2), range(len(num2)-1, -1, -1)):
			temp = ['z'] * len(num2)
			# sum = [0] * len(num2)
			# Multiply bit in num1 with each bit in num2
			for bit_1, j in zip(reversed(num1), range(len(num1)-1, -1, -1)):
				print ("bit2: " + bit_2 + " bit1: " + bit_1)
				# temp[j] = int(num1[i]) and int(num2[j])
				temp[j] = "t" + str(self.__generate_id_index())
				if i == (len(num2) - 1):
					sum[j] = "a" + str(self.__generate_id_index())
					self.rules.append((sum[j], "z"))
				self.rules.append((temp[j], bit_1 + ", " + bit_2))
			for k in range(shift_index):
				suffix = str(self.__generate_id_index())
				temp.append("t" + suffix)
				self.rules.append(("t" + suffix, "z"))
				if i == (len(num2) - 1):
					# check if i == 0, then only do this in that case.
					# otherwise, use the resulting values from the previous sum.
					self.rules.append(("a" + suffix, "z"))
					sum.append("a" + suffix)
			shift_index = shift_index + 1
			# sum = construct_sum_var(len(temp), str(i))]
			# print ("SUM: " + str(sum))
			print ("Sum: " + str(sum))
			sum = self._add(sum, temp)
			print ("Sum: " + str(sum))
		return sum[-self.size:]
		# print ("final sum: " + str(sum))

	def print_rules(self, f):
		for rule in self.rules:
			# print (rule[0] + " :- " + rule[1] + ".")
			f.write(rule[0] + " :- " + rule[1] + ".")
			f.write("\n")

	######################
	#					 #
	# 'Private' Methods: #
	#                    #
	######################

	def __full_adder(self, a, b, c_in):

		# If adding two zeroes, we only care about the carry bit.
		if a == 'z' and b == 'z':
			return 'z', c_in
		'''
		TODO investigate: will this potentially create duplicate rule names?
		'''
		prefix = b[1:]
		if prefix == "":
			prefix = str(self.__generate_id_index())

		self.rules.append(("i" + prefix, a + ", not " + b))
		self.rules.append(("i" + prefix, b + ", not " + a))
		self.rules.append(("s" + prefix, "i" + str(prefix) + ", not " + c_in))
		self.rules.append(("s" + prefix, c_in + ", not " + "i" + str(prefix)))
		self.rules.append(("c" + prefix, a + ", " + b))
		self.rules.append(("c" + prefix, c_in + ", " + str("i" + str(prefix))))
		return str("s" + prefix), str("c" + prefix)

	def __generate_id_index(self):
		self.var_id += 1
		return self.var_id

	def __resolve_lengths(self, num1, num2):
		diff = abs(len(num1) - len(num2))
		zeroes = ['z'] * diff
		if len(num1) > len(num2):
			num2 = zeroes + num2
		else:
			num1 = zeroes + num1
		return num1, num2

	def print_if(self, statement):
		if self.verbose:
			print(statement)
