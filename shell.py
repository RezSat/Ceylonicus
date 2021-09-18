from lexer import Lexer
from _parser import Parser
from interpreter import Interpreter, Context, global_symbol_table


def run(fn, text):
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


f = open('_printed_', 'w')
f.close()
text = open('somefile', 'r', encoding='utf-8').read()
if u'﻿' in text:
  text = text.replace(u'﻿', "")
result, error = run('<stdin>', text)

if error:
	print(error.as_string())
elif result:
	if len(result.elements) == 1:
		print(repr(result.elements[0]))
else:
	print(repr(result))
