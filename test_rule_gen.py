from rule_gen import RuleGenerator
import subprocess
from subprocess import DEVNULL

rule_gen = RuleGenerator(_verbose = True)

def convert_binary_to_vars(binary, prefix):
	vars = []
	for i in range(len(binary)):
		if binary[i] == '1':
			vars.append(prefix + str(len(binary) - i - 1))
	return vars

def get_clingo_result(output):
	prev = ""
	for line in output:
		if "Answer" in prev:
			return line.split()
		prev = line
	return None

def run_clingo(filename, args = []):
	try:
		clingo_output = subprocess.check_output(["clingo", filename, *args], stderr=DEVNULL)
		true_atoms = get_clingo_result(clingo_output)
	except subprocess.CalledProcessError as e:
		output = str(e.output)
		finished = output.split("\\n")
		true_atoms = get_clingo_result(finished)
	return true_atoms

num1 = ['x3', 'x2', 'x1', 'x0']
num2 = ['y3', 'y2', 'y1', 'y0']

f = open("meow.lp", "w+")

result = rule_gen.multiply(num1, num2)

print ("result: " + str(result))

rule_gen.print_rules(f)

vars = convert_binary_to_vars("0011", "x")
vars.extend(convert_binary_to_vars("1111", "y"))



for var in vars:
	f.write(var + ".\n")



f.write ("#show s.\n")

f.close()

atoms = run_clingo("meow.lp")

print ("atoms: " + str(atoms))

for var in result:
	if var in atoms:
		print (1, end =" ")
	else:
		print (0, end =" ")
print()

# THIS IS WORKING WITH NEGATIVE NUMBERS NOW I JUST NESLICED END OF THE MULTIPLY AND THAT IS IT!
#
#
