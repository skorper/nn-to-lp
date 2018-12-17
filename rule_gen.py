from operator import xor
import collections

class RuleGenerator(object):

	def __init__(self, _k, _size = 8, _rules = [], _var_id = 0, _verbose = False):
		self.rules = _rules
		self.var_id = _var_id
		self.verbose = _verbose
		self.size = _size
		self.k = _k

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
		if len(num1) > len(num2):
			temp = num1
			num1 = num2
			num2 = temp
		self.print_if ("Multiplying " + str(num1) + " and " + str(num2))
		shift_index = 0
		# sign_index = len(num2) - 1
		# sign_var = 

		#sign extend both nums
		num1_se = "n" + str(self.__generate_id_index())
		num2_se = "n" + str(self.__generate_id_index())

		self.rules.append((num1_se, num1[0]))
		self.rules.append((num2_se, num2[0]))

		num1 = [str(num1_se)] * len(num1) + num1
		num2 = [str(num2_se)] * len(num2) + num2


		sum = ["z"] * len(num2)
		for bit_2, i in zip(reversed(num2), range(len(num2)-1, -1, -1)):
			temp = ['z'] * len(num2)
			sign_vars = []
			# sum = [0] * len(num2)
			# Multiply bit in num1 with each bit in num2
			for bit_1, j in zip(reversed(num1), range(len(num1)-1, -1, -1)):
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

			# sign_vars = ["n" + str(self.__generate_id_index())] * sign_index
			# for sign_var in sign_vars:
			# 	self.rules.append((sign_var, bit_2 + ", " + num1[0] + ", not " + num2[0]))
			# temp = sign_vars + temp

			# print (temp)
			# print (sign_vars)
			shift_index += 1
			# sign_index -= 1
			
			# sum = construct_sum_var(len(temp), str(i))]
			# print ("SUM: " + str(sum))
			sum = self._add(sum, temp)
		# remove k elements from the end
		sum = sum[:-self.k]
		# only return the max num of bits
		return sum[-self.size:]
		# print ("final sum: " + str(sum))

	def print_rules(self, f=None):
		for rule in self.rules:
			if f == None:
				print (rule[0] + " :- " + rule[1] + ".")
			else:
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