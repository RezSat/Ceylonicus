import re
import string
try:
  from errors import IllegalCharError, InvalidSyntaxError, ExpectedCharError, RTError
  from tokens import Tokens, KEYWORDS, DIGITS, CHARACTERS, BuiltIns
except:
  from .errors import IllegalCharError, InvalidSyntaxError, ExpectedCharError, RTError
  from .tokens import Tokens, KEYWORDS, DIGITS, CHARACTERS, BuiltIns

#######################################
# POSITION
#######################################

class Position:
  """ 
  Position Class: As a Helper Class
  ______________________

  Use to get, copy the Position of a Character/Current Character,
  idx -> index
  ln -> line number,
  col -> column number
  fn -> filename, 
  ftxt -> file text /file content,

  advance() -> Go to next Character/Position
  copy() -> keep a record of the character position

  """
  def __init__(self, idx, ln, col, fn, ftxt):
    self.idx = idx
    self.ln = ln
    self.col = col
    self.fn = fn
    self.ftxt = ftxt

  def advance(self, current_char=None):
    self.idx += 1
    self.col += 1

    if current_char == '\n':
      self.ln += 1
      self.col = 0

    return self

  def copy(self):
    return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)

class Token:
  """
  Token Class
  ___________

  Keep a record of Token type->type_, value, start position->pos_start, end position->pos_end

  matches() -> match Token type to value and wise versa
  __repr__ -> if there is a Token Value : 'TOKEN_TYPE:TOKEN_VALUE' otherwise 'TOKEN_TYPE'

  """
  def __init__(self, type_, value=None, pos_start=None, pos_end=None):
    self.type = type_
    self.value = value

    if pos_start:
      self.pos_start = pos_start.copy()
      self.pos_end = pos_start.copy()
      self.pos_end.advance()

    if pos_end:
      self.pos_end = pos_end.copy()

  def matches(self, type_, value):
    return self.type == type_ and self.value == value
  
  def __repr__(self):
    if self.value: return f'{self.type}:{self.value}'
    return f'{self.type}'

#######################################
# LEXER
#######################################

class Lexer:
  """
  Lexer Class
  ___________

  create_tokens()->make a list of tokens. RETURN : LIST[TOKENS]
  create_number()->make floats and integers. RETURN : FLOAT | INTEGER
  create_string()->make strings that are between double quotes. RETURN : STRING
  create_identifier()->make identifier or reserved keyword. RETURN : IDENTIFIER | KEYWORD
  create_minus_or_arrow()->make minus symbol or arrow symbol. RETURN : MINUS | ARROW
  create_not_equals()->make not equals symbol. RETURN : NOTEQ
  create_less_than()->make less than symbol. RETURN : LESSTHAN | LTEQ
  create_greater_than()->make greater than  symbol. RETURN : GREATERTHAN | GTEQ
  create_equals()->make equal and equal euqal  symbol. RETURN : EQ | EQEQ
  skip_comment()-> Skip Comment : Commet starts with '#'
  """
  def __init__(self, fn, text):
    self.fn = fn
    self.text = text
    self.pos = Position(-1, 0, -1, fn, text)
    self.current_char = None
    self.advance()
  
  def advance(self):
    self.pos.advance(self.current_char)
    self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

  def create_tokens(self):
    tokens = []

    while self.current_char != None:
      if self.current_char in ' \t':
        self.advance()
      elif self.current_char == '#':
        self.skip_comment()
      elif self.current_char in ';\n':
        tokens.append(Token(Tokens['NEWLINE'], pos_start=self.pos))
        self.advance()
      elif self.current_char in re.findall(DIGITS, self.current_char) + ['.']:
        tokens.append(self.create_number())
      elif self.current_char in re.findall(CHARACTERS, self.current_char):
        tokens.append(self.create_identifier())
      elif self.current_char == '"':
        tokens.append(self.create_string())
      elif self.current_char == "'":
        tokens.append(self.create_string())
      elif self.current_char == "`":
        tokens.append(self.python_code())
      elif self.current_char == '+':
        tokens.append(Token(Tokens['PLUS'], pos_start=self.pos))
        self.advance()
      elif self.current_char == '-':
        tokens.append(self.create_minus_or_arrow())
      elif self.current_char == '*':
        tokens.append(Token(Tokens['MUL'], pos_start=self.pos))
        self.advance()
      elif self.current_char == '/':
        tokens.append(Token(Tokens['DIV'], pos_start=self.pos))
        self.advance()
      elif self.current_char == '^':
        tokens.append(Token(Tokens['POWER'], pos_start=self.pos))
        self.advance()
      elif self.current_char == '(':
        tokens.append(Token(Tokens['LPAREN'], pos_start=self.pos))
        self.advance()
      elif self.current_char == ')':
        tokens.append(Token(Tokens['RPAREN'], pos_start=self.pos))
        self.advance()
      elif self.current_char == '[':
        tokens.append(Token(Tokens['LSQUARE'], pos_start=self.pos))
        self.advance()
      elif self.current_char == ']':
        tokens.append(Token(Tokens['RSQUARE'], pos_start=self.pos))
        self.advance()
      elif self.current_char == '!':
        token, error = self.create_not_equals()
        if error: return [], error
        tokens.append(token)
      elif self.current_char == '=':
        tokens.append(self.create_equals())
      elif self.current_char == '<':
        tokens.append(self.create_less_than())
      elif self.current_char == '>':
        tokens.append(self.create_greater_than())
      elif self.current_char == ',':
        tokens.append(Token(Tokens['COMMA'], pos_start=self.pos))
        self.advance()
      else:
        pos_start = self.pos.copy()
        char = self.current_char
        self.advance()
        return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")

    tokens.append(Token(Tokens['EOF'], pos_start=self.pos))
    return tokens, None

  def create_number(self):
    num_str = ''
    dot_count = 0
    pos_start = self.pos.copy()


    while self.current_char != None and self.current_char in re.findall(DIGITS, self.current_char) + ['.']:
      if self.current_char == '.':
        if dot_count == 1: break
        dot_count += 1
      num_str += self.current_char
      self.advance()

    if dot_count == 0:
      return Token(Tokens['INT'], int(num_str), pos_start, self.pos)
    else:
      return Token(Tokens['FLOAT'], float(num_str), pos_start, self.pos)

  def create_string(self):
    string = ''
    pos_start = self.pos.copy()
    escape_character = False
    self.advance()

    escape_characters = {
      'n': '\n',
      't': '\t'
    }

    while self.current_char != None and self.current_char != '"' and self.current_char != "'" and self.current_char != escape_character:
      if escape_character:
        string += escape_characters.get(self.current_char, self.current_char)
      else:
        if self.current_char == '\\':
          escape_character = True
        else:
          string += self.current_char
      self.advance()
      escape_character = False

    self.advance()
    return Token(Tokens['STRING'], string, pos_start, self.pos)

  def python_code(self):
    python_string = ''
    pos_start = self.pos.copy()
    self.advance()

    while self.current_char != None and self.current_char != "`":
      python_string += self.current_char
      self.advance()

    self.advance()
    return Token(Tokens['PYTHON_CODE'], python_string, pos_start, self.pos)
  
  def create_identifier(self):
    id_str = ''
    pos_start = self.pos.copy()

    while self.current_char != None and self.current_char in re.findall(CHARACTERS, self.current_char):
      id_str += self.current_char
      self.advance()

    tok_type = Tokens['KEYWORD'] if id_str in KEYWORDS else Tokens['ID']
    if tok_type == "IDENTIFIER":
      if id_str in BuiltIns['null']:
        id_str = "null"
      if id_str in BuiltIns['false']:
        id_str = "false"
      if id_str in BuiltIns['true']:
        id_str = "true"
      if id_str in BuiltIns['math_pi']:
        id_str = "math_pi"
      if id_str in BuiltIns['write']:
        id_str = "write"
      if id_str in BuiltIns['input']:
        id_str = "input"
      if id_str in BuiltIns['int_input']:
        id_str = "int_input"
      if id_str in BuiltIns['clear']:
        id_str = "clear"
      if id_str in BuiltIns['is_num']:
        id_str = "is_num"
      if id_str in BuiltIns['is_str']:
        id_str = "is_str"
      if id_str in BuiltIns['is_list']:
        id_str = "is_list"
      if id_str in BuiltIns['is_function']:
        id_str = "is_function"
      if id_str in BuiltIns['to_str']:
        id_str = "to_str"
      if id_str in BuiltIns['to_num']:
        id_str = "to_num"
      if id_str in BuiltIns['type']:
        id_str = "type"
      if id_str in BuiltIns['append']:
        id_str = "append"
      if id_str in BuiltIns['pop']:
        id_str = "pop"
      if id_str in BuiltIns['extend']:
        id_str = "extend"
      if id_str in BuiltIns['len']:
        id_str = "len"
      if id_str in BuiltIns['import']:
        id_str = "import"

    return Token(tok_type, id_str, pos_start, self.pos)

  def create_minus_or_arrow(self):
    tok_type = Tokens['MINUS']
    pos_start = self.pos.copy()
    self.advance()

    if self.current_char == '>':
      self.advance()
      tok_type = Tokens['ARROW']
    return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

  def create_not_equals(self):
    pos_start = self.pos.copy()
    self.advance()

    if self.current_char == '=':
      self.advance()
      return Token(Tokens['NOTEQ'], pos_start=pos_start, pos_end=self.pos), None

    self.advance()
    return None, ExpectedCharError(pos_start, self.pos, "'=' (after '!')")
  
  def create_less_than(self):
    tok_type = Tokens['LESSTHAN']
    pos_start = self.pos.copy()
    self.advance()

    if self.current_char == '=':
      self.advance()
      tok_type = Tokens['LTEQ']

    return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

  def create_greater_than(self):
    tok_type = Tokens['GREATERTHAN']
    pos_start = self.pos.copy()
    self.advance()

    if self.current_char == '=':
      self.advance()
      tok_type = Tokens['GTEQ']

    return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

  def create_equals(self):
    tok_type = Tokens['EQ']
    pos_start = self.pos.copy()
    self.advance()

    if self.current_char == '=':
      self.advance()
      tok_type = Tokens['EQEQ']

    return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

  def skip_comment(self):
    self.advance()

    while self.current_char != '#':
      self.advance()

    self.advance()
