import enum
import sys

class Lexer:
	def __init__(self, source):
		# append a newline to the end of the source for parsing purposes
		self.source = source + '\n'
		# the current character value - don't pollute with bounds checking
		self.curChar = ''
		# the current position in the source string input
		self.curPos = -1
		# call for the next character
		self.nextChar()

	# process next character
	def nextChar(self):
		self.curPos += 1
		# if the cursor position is larger than the source, we've reached the end
		if self.curPos >= len(self.source):
			self.curChar = '\0'	# End Of File EOF denoted by null char
		else:
			self.curChar = self.source[self.curPos]

	# return the lookahead character
	def peek(self):
		if self.curPos + 1 >= len(self.source):
			return '\0'	# we're at the end of the file, similar to nextChar
		else:
			return self.source[self.curPos+1]

	# error for invalid token
	def abort(self, message):
		sys.exit("Lexing error. " + message)

	# skip whitespace characters
	def skipWhitespace(self):
		while self.curChar == ' ' or self.curChar == '\t' or self.curChar == '\r':
			self.nextChar()

	# skip code comments
	def skipComment(self):
		if self.curChar == "#":
			while self.curChar != '\n':
				self.nextChar()

	# return next token - meat of the lexer - called every token for classification
	def getToken(self):
		self.skipWhitespace()
		self.skipComment()
		token = None
		# checks for operators, new lines, and EOF
		# if multichar operator, we process the remainder
		if self.curChar == '+':
			token = Token(self.curChar, TokenType.PLUS)
		elif self.curChar == '-':
			token = Token(self.curChar, TokenType.MINUS)
		elif self.curChar == '*':
			token = Token(self.curChar, TokenType.ASTERISK)
		elif self.curChar == '/':
			token = Token(self.curChar, TokenType.SLASH)
		elif self.curChar == '=':
			# peek ahead to see if the next character is also part of the operator
			if self.peek() == '=':
				lastChar = self.curChar
				self.nextChar()
				token = Token(lastChar + self.curChar, TokenType.EQEQ)
			else:
				token = Token(self.curChar, TokenType.EQ)
		elif self.curChar == '>':
			if self.peek() == '=':
				lastChar = self.curChar
				self.nextChar()
				token = Token(lastChar + self.curChar, TokenType.GTEQ)
			else:
				token = Token(self.curChar, TokenType.GT)
		elif self.curChar == '<':
			if self.peek() == '=':
				lastChar = self.curChar
				self.nextChar()
				token = Token(lastChar + self.curChar, TokenType.LTEQ)
			else:
				token = Token(self.curChar, TokenType.LT)
		elif self.curChar == '!':
			if self.peek() == '=':
				lastChar = self.curChar
				self.nextChar()
				token = Token(lastChar + self.curChar, TokenType.NOTEQ)
			else:
				self.abort("Expected !=, got !" + self.peek())
		elif self.curChar == '\n':
			token = Token(self.curChar, TokenType.NEWLINE)
		elif self.curChar == '\0':
			token = Token(self.curChar, TokenType.EOF) # EOF
		elif self.curChar == '\"':
			self.nextChar()
			startPos = self.curPos

			while self.curChar != '\"':
				# don't allow special characters in strings so we can compile to c
				if self.curChar == '\r' or self.curChar == '\n' or self.curChar == '\t' or self.curChar == '\\' or self.curChar == '%':
					self.abort("Illegal character in string.")
				self.nextChar()

			tokText = self.source[startPos : self.curPos] # gets the substring
			token = Token(tokText, TokenType.STRING)
		elif self.curChar.isdigit():
			startPos = self.curPos
			while self.peek().isdigit():
				self.nextChar()
			if self.peek() == '.': # decimal number
				self.nextChar()

				if not self.peek().isdigit():
					# Error, not a proper decimal number
					self.abort("Illegal char in number.")
				while self.peek().isdigit():
					self.nextChar()
			tokText = self.source[startPos : self.curPos + 1] # get substring for number
			token = Token(tokText, TokenType.NUMBER)
		elif self.curChar.isalpha():
			startPos = self.curPos
			while self.peek().isalnum():
				self.nextChar()

			tokText = self.source[startPos : self.curPos + 1] # get substring
			# this allows us to define additional keywords in our token class
			keyword = Token.checkIfKeyword(tokText)
			if keyword == None:
				token = Token(tokText, TokenType.IDENT)
			else:
				# if it's a keyword, use the keyword as the TokenType
				token = Token(tokText, keyword)

		else:
			self.abort("Unknown token: " + self.curChar) # Error, unknown token
		
		self.nextChar()
		return token

class Token:
	def __init__(self, tokenText, tokenKind):
		self.text = tokenText # actual text of the token
		self.kind = tokenKind # type of token
	
	@staticmethod
	def checkIfKeyword(tokenText):
		for kind in TokenType:
			# all keyword enum values must be of value 1XX
			if kind.name == tokenText and kind.value >= 100 and kind.value < 200:
				return kind
		return None

# TokenType is the enum for all token types encounterable in our language
class TokenType(enum.Enum):
	EOF = -1
	NEWLINE = 0
	NUMBER = 1
	IDENT = 2
	STRING = 3
	# keywords section
	LABEL = 101
	GOTO = 102
	PRINT = 103
	INPUT = 104
	LET = 105
	IF = 106
	THEN = 107
	ENDIF = 108
	WHILE = 109
	REPEAT = 110
	ENDWHILE = 111
	# operators section
	EQ = 201 # single equals for assignment
	PLUS = 202
	MINUS = 203
	ASTERISK = 204
	SLASH = 205
	EQEQ = 206 # double equals for comparison
	NOTEQ = 207
	LT = 208 # LESSTHAN
	LTEQ = 209
	GT = 210 # GREATERTHAN
	GTEQ = 211