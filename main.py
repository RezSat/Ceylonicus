try:
  from lexer import Lexer
  from _parser import Parser
  from interpreter import Interpreter, Context, global_symbol_table
except:
  from .lexer import Lexer
  from ._parser import Parser
  from .interpreter import Interpreter, Context, global_symbol_table

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