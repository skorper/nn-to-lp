from rule_gen import RuleGenerator
rule_gen = RuleGenerator(_verbose = False)

num1 = ['x3', 'x2', 'x1', 'x0']
num2 = ['y3', 'y2', 'y1', 'y0']

print ("%" + str(rule_gen.multiply(num1, num2)))
rule_gen.print_rules()

print ("x3.")
print ("x1.")
print ("y3.")
print ("y0.")

print ("#show s.")