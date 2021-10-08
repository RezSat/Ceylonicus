try:
  from lexer import Lexer
  from _parser import Parser
  from interpreter import Interpreter, Context, global_symbol_table
except:
  from .lexer import Lexer
  from ._parser import Parser
  from .interpreter import Interpreter, Context, global_symbol_table
import sys

def Execute(fn, text):
  f = open("_printed_",'w')
  f.close()
  # Generate tokens
  lexer = Lexer(fn, text)
  tokens, error = lexer.create_tokens()
  if error: return None, error
  
  # Generate AST
  parser = Parser(tokens)
  ast = parser.parse()
  if ast.error: return None, ast.error

  # Run program
  interpreter = Interpreter()
  context = Context('<program>')
  context.symbol_table = global_symbol_table
  result = interpreter.visit(ast.node, context)

  return result.value, result.error

if __name__ == '__main__':
  if sys.argv[1] == None or "":
    print("No file provided!.")
  else:
    text = open(sys.argv[1], 'r', encoding="utf-8").read()
    if u'﻿' in text:
      text = text.replace(u'﻿', "")
    if u'﻿' in text:
      text = text.replace(u'﻿', "")

    result, error = Execute('<stdin>', text)

    if error:
      print(error.as_string())
    elif result:
      if len(result.elements) == 1:
        print(repr(result.elements[0]))
    else:
      print(repr(result))