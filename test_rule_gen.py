from rule_gen import RuleGenerator
import subprocess
from subprocess import DEVNULL
from converter import Converter

rule_gen = RuleGenerator(_verbose = False)

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

vars = convert_binary_to_vars("0110", "x")
vars.extend(convert_binary_to_vars("1111", "y"))

for var in vars:
	f.write(var + ".\n")

f.write ("#show s.\n")

f.close()

atoms = run_clingo("meow.lp")

# print ("atoms: " + str(atoms))
original_lp_result = ""

for var in result:
	if var in atoms:
		# print (1, end =" ")
		original_lp_result += "1"
	else:
		# print (0, end =" ")
		original_lp_result += "0"
print()

converter = Converter("_ch")
converter.convert_to("meow.lp")

try:
	cmd = ['java', 'SimplifyProgramInput_2', 'meow_ch.lp', 'meow_ch_simp.lp']
	subprocess.check_output(cmd)#, stderr=DEVNULL)
except subprocess.CalledProcessError as e:
	print ("Error: " + str(e))


converter.convert_from("meow_ch_simp.lp")

atoms_simplified = run_clingo("meow_simp.lp")
simplified_lp_result = ""

for var in result:
	if var in atoms_simplified:
		# print (1, end =" ")
		simplified_lp_result += "1"
	else:
		# print (0, end =" ")
		simplified_lp_result += "0"

print ("original logic program result:   " + original_lp_result)
print ("simplified logic program result: " + simplified_lp_result)
if original_lp_result != simplified_lp_result:
	print ("They do not match. Therefore, the simplified logic program does not represent the same rules.")
else:
	print ("They match. Therefore, the simplified logic program represents the same rules.")