from operator import xor
import collections

'''
For now, just an incrementer. TODO: add something a bit more involved.
'''
def generate_id():
	global var_id
	var_id += 1
	# print ("var_id: " + str(var_id))
	return var_id

'''
Check if they are the same length, if not add padding.
'''
def same_length(num1, num2):
	if len(num1) > len(num2):
		diff = len(num1) - len(num2)
		for i in range(diff):
			num2 = [0] + num2
	if len(num1) < len(num2):
		diff = len(num2) - len(num1)
		for i in range(diff):
			num1 = [0] + num1
	return num1, num2

'''
Return SUM, CARRY
'''
def full_adder(a, b, c_in):
	prefix = b[1:]
	# print ("prefix: " + str(prefix))
	rules.append(("i" + prefix, a + ", not " + b))
	rules.append(("i" + prefix, b + ", not " + a))
	rules.append(("s" + prefix, "i" + str(prefix) + ", not " + c_in))
	rules.append(("s" + prefix, c_in + ", not " + "i" + str(prefix)))
	rules.append(("c" + prefix, a + ", " + b))
	rules.append(("c" + prefix, c_in + ", " + str("i" + str(prefix))))
	return str("s" + prefix), str("c" + prefix)

def add(num1, num2):
	# print ("adding " + str(num1) + " and " + str(num2))
	# num1, num2 = same_length(num1, num2)
	# sum holds the vars which the result was placed into (for next comp)
	sum = [None] * int(len(max(num1, num2)) + 1)
	c = "0"
	for i in range(len(num1) - 1, -1, -1):
		s, c = full_adder(str(num1[i]), str(num2[i]), c)
		sum[i+1] = s
	sum[0] = c
	# print ("sum: " + str(sum))
	return sum

'''
num1: shorter num
Unfortunately this isn't as pretty as the adder, but it would increase
complexity to calculate each bit at a time because the carry can be > 1
'''
def multiply(num1, num2):
	print ("Multiplying " + str(num1) + " and " + str(num2))
	shift_index = 0
	sum = ["0"] * len(num2)
	for bit_2, i in zip(num2, range(len(num2))):
		temp = [0] * len(num2)
		# sum = [0] * len(num2)
		# Multiply bit in num1 with each bit in num2
		for bit_1, j in zip(num1, range(len(num1))):
			# temp[j] = int(num1[i]) and int(num2[j])
			temp[j] = "t" + str(generate_id())
			if i == 0:
				sum[j] = "a" + str(generate_id())
				rules.append((sum[j], "0"))
			rules.append((temp[j], bit_1 + ", " + bit_2))
		for k in range(shift_index):
			suffix = str(generate_id())
			temp.append("t" + suffix)
			rules.append(("t" + suffix, "0"))
			if i == 0:
				# check if i == 0, then only do this in that case.
				# otherwise, use the resulting values from the previous sum.
				rules.append(("a" + suffix, "0"))
				sum.append("a" + suffix)
		shift_index = shift_index + 1
		# sum = construct_sum_var(len(temp), str(i))]
		# print ("SUM: " + str(sum))
		sum = add(sum, temp)
	print ("final sum: " + str(sum))
	# return sum

num1 = ["a1", "a0"]  
num2 = ["b1", "b0"]

var_id = len(max(num1, num2))
rules = []

multiply(num1, num2)

for rule in rules:
	# if rule[0][0] == 's':
	print (rule[0] + " <-- " + rule[1])