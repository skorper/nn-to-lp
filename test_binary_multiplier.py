from operator import xor

'''
Check if they are the same length, if not add 0's
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
	intermediate = xor(a, b)
	sum = xor(intermediate, c_in)
	carry = a and b or (c_in and intermediate)
	return sum, carry

def add(num1, num2):
	num1, num2 = same_length(num1, num2)
	cin = 0
	res = [None] * len(num1)
	for i in range(len(num1) - 1, -1, -1):
		res[i], cin = full_adder(num1[i], num2[i], cin)
	# Only append carry bit if it's 1
	if cin:
		res = [cin] + res
	return res

'''
num1: shorter num
Unfortunately this isn't as pretty as the adder, but it would increase
complexity to calculate each bit at a time because the carry can be > 1
'''
def multiply(num1, num2):
	sum = [0]
	shift_index = 0
	for i in range(len(num1) - 1, -1, -1):
		temp = [0] * len(num2)
		# Multiply bit in num1 with each bit in num2
		for j in range (len(num2) - 1, -1, -1):
			temp[j] = int(num1[i]) and int(num2[j])
		for k in range(shift_index):
			temp.append(0)
		shift_index = shift_index + 1
		sum = add(sum, temp)
	return sum


num1 = [1, 1, 0, 1]
num2 = [1, 1, 0, 1]

print (multiply(num1, num2))
