# Teeny Tiny Compiler
# Original tutorial by https://austinhenley.com/blog/teenytinycompiler1.html
# Modifications by Keaton Tate

from lex import *

def main():
	source = "IF+-123 foo*THEN/"
	lexer = Lexer(source)

	token = lexer.getToken()
	while token.kind != TokenType.EOF:
		print(token.kind)
		token = lexer.getToken()

main()