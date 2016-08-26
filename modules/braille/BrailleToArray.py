class Grade2BrailleCharacter:
	"""
		Accepts an alphanumeric character and returns a six element array
		indicating 'dot' arrangement
	"""

	def __init__( self, ascii_char ):
		self.ascii_char = ascii_char
		self._dot_code = self._get_dots(ascii_char)

	def _get_dots( self, ascii_char ):
		dot_code = [0, 0, 0, 0, 0, 0]

		if ascii_char == 'a':
			dot_code = [1, 0, 0, 0, 0, 0]
		elif ascii_char == 'b':
			dot_code = [1, 1, 0, 0, 0, 0]
		elif ascii_char == 'c':
			dot_code = [1, 0, 0, 1, 0, 0]
		elif ascii_char == 'd':
			dot_code = [1, 0, 0, 1, 1, 0]
		elif ascii_char == 'e':
			dot_code = [1, 0, 0, 0, 1, 0]
		elif ascii_char == 'f':
			dot_code = [1, 1, 0, 1, 0, 0]
		elif ascii_char == 'g':
			dot_code = [1, 1, 0, 1, 1, 0]
		elif ascii_char == 'h':
			dot_code = [1, 1, 0, 0, 1, 0]
		elif ascii_char == 'i':
			dot_code = [0, 1, 0, 1, 0, 0]
		elif ascii_char == 'j':
			dot_code = [0, 1, 0, 1, 1, 0]
		elif ascii_char == 'k':
			dot_code = [1, 0, 1, 0, 0, 0]
		elif ascii_char == 'l':
			dot_code = [1, 1, 1, 0, 0, 0]
		elif ascii_char == 'm':
			dot_code = [1, 0, 1, 1, 0, 0]
		elif ascii_char == 'n':
			dot_code = [1, 0, 1, 1, 1, 0]
		elif ascii_char == 'o':
			dot_code = [1, 0, 1, 0, 1, 0]
		elif ascii_char == 'p':
			dot_code = [1, 1, 1, 1, 0, 0]
		elif ascii_char == 'q':
			dot_code = [1, 1, 1, 1, 1, 0]
		elif ascii_char == 'r':
			dot_code = [1, 1, 1, 0, 1, 0]
		elif ascii_char == 's':
			dot_code = [0, 1, 1, 1, 0, 0]
		elif ascii_char == 't':
			dot_code = [0, 1, 1, 1, 1, 0]
		elif ascii_char == 'u':
			dot_code = [1, 0, 1, 0, 0, 1]
		elif ascii_char == 'v':
			dot_code = [1, 1, 1, 0, 0, 1]
		elif ascii_char == 'w':
			dot_code = [0, 1, 0, 1, 1, 1]
		elif ascii_char == 'x':
			dot_code = [1, 0, 1, 1, 0, 1]
		elif ascii_char == 'y':
			dot_code = [1, 0, 1, 1, 1, 1]
		elif ascii_char == 'z':
			dot_code = [1, 0, 1, 0, 1, 1]
		elif ascii_char == '1':
			dot_code = [1, 0, 0, 0, 0, 0]
		elif ascii_char == '2':
			dot_code = [1, 1, 0, 0, 0, 0]
		elif ascii_char == '3':
			dot_code = [1, 0, 0, 1, 0, 0]
		elif ascii_char == '4':
			dot_code = [1, 0, 0, 1, 1, 0]
		elif ascii_char == '5':
			dot_code = [1, 0, 0, 0, 1, 0]
		elif ascii_char == '6':
			dot_code = [1, 1, 0, 1, 0, 0]
		elif ascii_char == '7':
			dot_code = [1, 1, 0, 1, 1, 0]
		elif ascii_char == '8':
			dot_code = [1, 1, 0, 1, 0, 0]
		elif ascii_char == '9':
			dot_code = [0, 1, 0, 1, 0, 0]
		elif ascii_char == '0':
			dot_code = [0, 1, 0, 1, 1, 0]

		return dot_code

	@property
	def dot_code( self ):
		return self._dot_code

class BrailleSequence:
	def __init__( self, text ):
		self._braille_characters = []
		for char in text:
			self._braille_characters.append(Grade2BrailleCharacter(char))

	@property
	def braille_characters( self ):
		return self._braille_characters
