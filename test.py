try:
  from lexer import Lexer
  from _parser import Parser
  from interpreter import Interpreter, Context, global_symbol_table
except:
  from .lexer import Lexer
  from ._parser import Parser
  from .interpreter import Interpreter, Context, global_symbol_table

def run(fn, text):
  f = open('_printed_', 'w')
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


text = """
#paste your code here and run this file.

ආනයනය_කරන්න("examples/write.cyl")
var x = "100"
write(වර්ගය(x))
write("කරන්න")

"""
result, error = run('<stdin>', text)

if error:
	print(error.as_string())
elif result:
	if len(result.elements) == 1:
		print(repr(result.elements[0]))
else:
	print(repr(result))

print("Check `_printed_` file for printed info")
