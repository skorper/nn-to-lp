from operator import xor
from sympy import *

vars = set() #for fast and easy lookup!
rules = []

'''
Return SUM, CARRY
'''
def full_adder(a, b, c_in):
	rules.append(("i" + a[-1], a + " XOR " + b))
	# intermediate = xor(a, b)

	rules.append(("s" + a[-1], "i1 XOR " + c_in))
	# sum = xor(intermediate, c_in)

	rules.append(("c" + a[-1], a + " AND " + b + " OR ( " + c_in + " AND i1)"))
	# carry = a and b or (c_in and intermediate)
	# print (sum)
	# print (carry)
	# return sum, carry

num1 = "00101010"
num2 = "11110000"
cin = 0
res = [None] * len(num1)

test_len = 4
a = "a"
b = "b"
c = "c"

idx = 0

# first iteration gets 0 for cin^^
for i in range(test_len - 1, -1, -1):
	full_adder(a + str(idx), b + str(idx), c + str(idx))
	idx = idx + 1

for rule in rules:
	print (rule[0] + " <-- " + rule[1])

