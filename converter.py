class Converter(object):
	def __init__(self, _file_suffix):
		self.file_suffix = _file_suffix

	'''
	Convert file from clingo syntax to simplifier syntax
	'''
	def convert_to(self, file):
		f = open(file, "r")
		lines = f.readlines()
		f.close()

		filename = file.split(".")[0] + self.file_suffix + "." + file.split(".")[1]
		f = open(filename, "w+")

		for line in lines:
			f.write(self.convert_line_to(line))
		f.close()

	'''
	Convert file from simplifier syntax to clingo syntax
	'''
	def convert_from(self, file):
		f = open(file, "r")
		lines = f.readlines()
		f.close()

		filename = file.split("_")[0] + "_simp." + file.split(".")[1]
		f = open(filename, "w+")

		for line in lines:
			f.write(self.convert_line_from(line))
		f.close()

	'''
	Convert line from simplifier syntax to clingo syntax
	'''
	def convert_line_from(self, line):
		line = line[:-2] + "." + '\n'
		line = line.replace(":- ", ":-")
		LHS = line.split(":-")[0]
		RHS = line.split(":-")[1]
		RHS = RHS.replace(" ", ", ")
		RHS = RHS.replace("-", "not ")
		line = LHS + ":-" + RHS
		line = line.replace(":-", ":- ")
		return line

	'''
	Convert line from clingo syntax to simplifier syntax
	'''
	def convert_line_to(self, line):
		line = line.replace(".", "")
		line = line.replace(",", "")
		line = line.replace("not ", "-")
		return line

converter = Converter("_ch")
converter.convert_from("meow_ch_simp.lp")