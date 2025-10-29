# Teeny Tiny Compiler
# Original tutorial by https://austinhenley.com/blog/teenytinycompiler1.html
# Modifications by Keaton Tate

from lex import *
from parse import *

def main():
	print("Teeny Tiny Compiler")

	if len(sys.argv) != 2:
		sys.exit("Error: Compiler needs source file as argument.")
	with open(sys.argv[1], 'r') as inputFile:
		source = inputFile.read()

	# Initialize the lexer and parser
	lexer = Lexer(source)
	parser = Parser(lexer)

	parser.program()
	print("Parsing completed")

main()