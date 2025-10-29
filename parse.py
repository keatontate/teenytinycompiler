import sys
from lex import *

class Parser:
	"""docstring for Parser"""
	def __init__(self, lexer):
		self.lexer = lexer

		self.curToken = None
		self.peekToken = None
		self.nextToken()
		self.nextToken() # initializes current and peek when calling twice

	def checkToken(self, kind):
		return kind == self.curToken.kind

	def checkPeek(self, kind):
		return kind == self.peekToken.kind

	def match(self, kind):
		if not self.checkToken(kind):
			self.abort("Expected " + kind.name + ", got " + self.curToken.kind.name)
		self.nextToken()

	def nextToken(self):
		self.curToken = self.peekToken
		self.peekToken = self.lexer.getToken()

	def abort(self, message):
		sys.exit("Error. " + message)

	def program(self):
		print("PROGRAM")

		while self.checkToken(TokenType.NEWLINE):
			self.nextToken()

		while not self.checkToken(TokenType.EOF):
			self.statement()

	def statement(self):
		if self.checkToken(TokenType.PRINT):
			print("STATEMENT-PRINT")
			self.nextToken()

			if self.checkToken(TokenType.STRING):
				self.nextToken()
			else:
				self.expression()

		elif self.checkToken(TokenType.IF):
			print("STATEMENT-IF")
			self.nextToken()
			self.comparison()

			self.match(TokenType.THEN)
			self.nl()

			# keep appending statements until we hit the ENDIF
			while not self.checkToken(TokenType.ENDIF):
				self.statement()

			# we expect an endif in the grammar
			self.match(TokenType.ENDIF)

		elif self.checkToken(TokenType.WHILE):
			print("STATEMENT-WHILE")
			self.nextToken()
			self.comparison()

			self.match(TokenType.REPEAT)
			self.nl()

			while not self.checkToken(TokenType.ENDWHILE):
				self.statement()

			self.match(TokenType.ENDWHILE)

		elif self.checkToken(TokenType.LABEL):
			print("STATEMENT-LABEL")
			self.nextToken()
			self.match(TokenType.IDENT)

		elif self.checkToken(TokenType.GOTO):
			print("STATEMENT-GOTO")
			self.nextToken()
			self.match(TokenType.IDENT)

		elif self.checkToken(TokenType.LET):
			print("STATEMENT-LET")
			self.nextToken()
			self.match(TokenType.IDENT)
			self.match(TokenType.EQ)
			self.expression()

		elif self.checkToken(TokenType.INPUT):
			print("STATEMENT-INPUT")
			self.nextToken()
			self.match(TokenType.IDENT)

		# should throw an error if we make a grammar mistake
		else:
			self.abort("Invalid statement at " + self.curToken.text + " (" + self.curToken.kind.name + ")")


		self.nl()

	def expression():
		pass
		# TODO - Parsing Expressions - https://austinhenley.com/blog/teenytinycompiler2.html

	def nl(self):
		print("NEWLINE")
		while self.checkToken(TokenType.NEWLINE):
			self.nextToken()