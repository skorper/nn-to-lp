from operator import xor

'''
Return SUM, CARRY
'''
def full_adder(a, b, c_in):
	intermediate = xor(a, b)
	sum = xor(intermediate, c_in)
	carry = a and b or (c_in and intermediate)
	print (sum)
	print (carry)
	return sum, carry

num1 = "00101010"
num2 = "11110000"
cin = 0
res = [None] * len(num1)

for i in range(len(num1) - 1, -1, -1):
	res[i], cin = full_adder(int(num1[i]), int(num2[i]), cin)
print (res)
print (cin)

