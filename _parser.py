import string
try:  
  from AST import NumberNode, BinOpNode, UnaryOpNode, StringNode, ListNode, VarAccessNode, VarAssignNode, IfNode, ForNode,WhileNode, FuncDefNode, CallNode, ReturnNode, ContinueNode, BreakNode
  from errors import InvalidSyntaxError
  from tokens import Tokens
except:
  from .AST import NumberNode, BinOpNode, UnaryOpNode, StringNode, ListNode, VarAccessNode, VarAssignNode, IfNode, ForNode,WhileNode, FuncDefNode, CallNode, ReturnNode, ContinueNode, BreakNode
  from .errors import InvalidSyntaxError
  from .tokens import Tokens

#######################################
# PARSE RESULT
#######################################

class ParseResult:
  def __init__(self):
    self.error = None
    self.node = None
    self.last_registered_advance_count = 0
    self.advance_count = 0
    self.to_reverse_count = 0

  def register_advancement(self):
    self.last_registered_advance_count = 1
    self.advance_count += 1

  def register(self, res):
    self.last_registered_advance_count = res.advance_count
    self.advance_count += res.advance_count
    if res.error: self.error = res.error
    return res.node

  def try_register(self, res):
    if res.error:
      self.to_reverse_count = res.advance_count
      return None
    return self.register(res)

  def success(self, node):
    self.node = node
    return self

  def failure(self, error):
    if not self.error or self.last_registered_advance_count == 0:
      self.error = error
    return self

#######################################
# PARSER
#######################################

class Parser:
  def __init__(self, tokens):
    self.tokens = tokens
    self.tok_idx = -1
    self.advance()

  def advance(self):
    self.tok_idx += 1
    self.update_current_tok()
    return self.current_tok

  def reverse(self, amount=1):
    self.tok_idx -= amount
    self.update_current_tok()
    return self.current_tok

  def update_current_tok(self):
    if self.tok_idx >= 0 and self.tok_idx < len(self.tokens):
      self.current_tok = self.tokens[self.tok_idx]

  def parse(self):
    res = self.statements()
    if not res.error and self.current_tok.type != Tokens['EOF']:
      return res.failure(InvalidSyntaxError(
        self.current_tok.pos_start, self.current_tok.pos_end,
        "Token cannot appear after previous tokens"
      ))
    return res

  ###################################

  def statements(self):
    res = ParseResult()
    statements = []
    pos_start = self.current_tok.pos_start.copy()

    while self.current_tok.type == Tokens['NEWLINE']:
      res.register_advancement()
      self.advance()

    statement = res.register(self.statement())
    if res.error: return res
    statements.append(statement)

    more_statements = True

    while True:
      newline_count = 0
      while self.current_tok.type == Tokens['NEWLINE']:
        res.register_advancement()
        self.advance()
        newline_count += 1
      if newline_count == 0:
        more_statements = False
      
      if not more_statements: break
      statement = res.try_register(self.statement())
      if not statement:
        self.reverse(res.to_reverse_count)
        more_statements = False
        continue
      statements.append(statement)

    return res.success(ListNode(
      statements,
      pos_start,
      self.current_tok.pos_end.copy()
    ))

  def statement(self):
    res = ParseResult()
    pos_start = self.current_tok.pos_start.copy()

    if (self.current_tok.matches(Tokens['KEYWORD'], 'return') or
        self.current_tok.matches(Tokens['KEYWORD'], 'දෙන්න')):
      res.register_advancement()
      self.advance()

      expr = res.try_register(self.expr())
      if not expr:
        self.reverse(res.to_reverse_count)
      return res.success(ReturnNode(expr, pos_start, self.current_tok.pos_start.copy()))
    
    if self.current_tok.matches(Tokens['KEYWORD'], 'දිගටම'):
      res.register_advancement()
      self.advance()
      if self.current_tok.matches(Tokens['KEYWORD'], 'කරන්න'):
        res.register_advancement()
        self.advance()
      else:
        return res.failure(InvalidSyntaxError(
          self.current_tok.pos_start, self.current_tok.pos_end,
          "Expected 'කරන්න'"
        ))

      return res.success(ContinueNode(pos_start, self.current_tok.pos_start.copy()))

    if self.current_tok.matches(Tokens['KEYWORD'], 'continue'):
      res.register_advancement()
      self.advance()

      return res.success(ContinueNode(pos_start, self.current_tok.pos_start.copy()))

    if (self.current_tok.matches(Tokens['KEYWORD'], 'break') or
        self.current_tok.matches(Tokens['KEYWORD'], 'නවත්වන්න')):
      res.register_advancement()
      self.advance()
      return res.success(BreakNode(pos_start, self.current_tok.pos_start.copy()))

    expr = res.register(self.expr())
    if res.error:
      return res.failure(InvalidSyntaxError(
        self.current_tok.pos_start, self.current_tok.pos_end,
        "Expected 'RETURN', 'CONTINUE', 'BREAK', 'VAR', 'IF', 'FOR', 'WHILE', 'FUN', int, float, identifier, '+', '-', '(', '[' or 'NOT'"
      ))
    return res.success(expr)

  def expr(self):
    res = ParseResult()
    if self.current_tok.matches(Tokens['KEYWORD'], 'var') or self.current_tok.matches(Tokens['KEYWORD'], 'විචල්ය') or self.current_tok.matches(Tokens['KEYWORD'], 'විචල්‍ය​'):
      res.register_advancement()
      self.advance()

      if self.current_tok.type != Tokens['ID']:
        return res.failure(InvalidSyntaxError(
          self.current_tok.pos_start, self.current_tok.pos_end,
          "Expected identifier"
        ))

      var_name = self.current_tok
      res.register_advancement()
      self.advance()

      if self.current_tok.type != Tokens['EQ']:
        return res.failure(InvalidSyntaxError(
          self.current_tok.pos_start, self.current_tok.pos_end,
          "Expected '='"
        ))

      res.register_advancement()
      self.advance()
      expr = res.register(self.expr())
      if res.error: return res
      return res.success(VarAssignNode(var_name, expr))

    node = res.register(self.bin_op(self.comp_expr, (
      (Tokens['KEYWORD'], 'and'),
      (Tokens['KEYWORD'], 'සහ'), 
      (Tokens['KEYWORD'], 'or'),
      (Tokens['KEYWORD'], 'හෝ'), 
      )))

    if res.error:
      return res.failure(InvalidSyntaxError(
        self.current_tok.pos_start, self.current_tok.pos_end,
        "Expected 'VAR', 'IF', 'FOR', 'WHILE', 'FUN', int, float, identifier, '+', '-', '(', '[' or 'NOT'"
      ))

    return res.success(node)

  def comp_expr(self):
    res = ParseResult()

    if self.current_tok.matches(Tokens['KEYWORD'], 'not') or self.current_tok.matches(Tokens['KEYWORD'], 'නොමැත') or self.current_tok.matches(Tokens['KEYWORD'], 'නොව') or self.current_tok.matches(Tokens['KEYWORD'], 'නැත') or self.current_tok.matches(Tokens['KEYWORD'], 'නොවේ') or self.current_tok.matches(Tokens['KEYWORD'], 'නොවන​'):
      op_tok = self.current_tok
      res.register_advancement()
      self.advance()

      node = res.register(self.comp_expr())
      if res.error: return res
      return res.success(UnaryOpNode(op_tok, node))
    
    node = res.register(self.bin_op(self.arith_expr, (Tokens['EQEQ'], Tokens['NOTEQ'], Tokens['LESSTHAN'], Tokens['GREATERTHAN'], Tokens['LTEQ'], Tokens['GTEQ'])))
    
    if res.error:
      return res.failure(InvalidSyntaxError(
        self.current_tok.pos_start, self.current_tok.pos_end,
        "Expected int, float, identifier, '+', '-', '(', '[', 'IF', 'FOR', 'WHILE', 'FUN' or 'NOT'"
      ))

    return res.success(node)

  def arith_expr(self):
    return self.bin_op(self.term, (Tokens['PLUS'], Tokens['MINUS']))

  def term(self):
    return self.bin_op(self.factor, (Tokens['MUL'], Tokens['DIV']))

  def factor(self):
    res = ParseResult()
    tok = self.current_tok

    if tok.type in (Tokens['PLUS'], Tokens['MINUS']):
      res.register_advancement()
      self.advance()
      factor = res.register(self.factor())
      if res.error: return res
      return res.success(UnaryOpNode(tok, factor))

    return self.power()

  def power(self):
    return self.bin_op(self.call, (Tokens['POWER'], ), self.factor)

  def call(self):
    res = ParseResult()
    atom = res.register(self.atom())
    if res.error: return res

    if self.current_tok.type == Tokens['LPAREN']:
      res.register_advancement()
      self.advance()
      arg_nodes = []

      if self.current_tok.type == Tokens['RPAREN']:
        res.register_advancement()
        self.advance()
      else:
        arg_nodes.append(res.register(self.expr()))
        if res.error:
          return res.failure(InvalidSyntaxError(
            self.current_tok.pos_start, self.current_tok.pos_end,
            "Expected ')', 'VAR', 'IF', 'FOR', 'WHILE', 'FUN', int, float, identifier, '+', '-', '(', '[' or 'NOT'"
          ))

        while self.current_tok.type == Tokens['COMMA']:
          res.register_advancement()
          self.advance()

          arg_nodes.append(res.register(self.expr()))
          if res.error: return res

        if self.current_tok.type != Tokens['RPAREN']:
          return res.failure(InvalidSyntaxError(
            self.current_tok.pos_start, self.current_tok.pos_end,
            f"Expected ',' or ')'"
          ))

        res.register_advancement()
        self.advance()
      return res.success(CallNode(atom, arg_nodes))
    return res.success(atom)

  def atom(self):
    res = ParseResult()
    tok = self.current_tok

    if tok.type in (Tokens['INT'], Tokens['FLOAT']):
      res.register_advancement()
      self.advance()
      return res.success(NumberNode(tok))

    elif tok.type == Tokens['STRING']:
      res.register_advancement()
      self.advance()
      return res.success(StringNode(tok))

    elif tok.type == Tokens['ID']:
      res.register_advancement()
      self.advance()
      return res.success(VarAccessNode(tok))

    elif tok.type == Tokens['LPAREN']:
      res.register_advancement()
      self.advance()
      expr = res.register(self.expr())
      if res.error: return res
      if self.current_tok.type == Tokens['RPAREN']:
        res.register_advancement()
        self.advance()
        return res.success(expr)
      else:
        return res.failure(InvalidSyntaxError(
          self.current_tok.pos_start, self.current_tok.pos_end,
          "Expected ')'"
        ))

    elif tok.type == Tokens['LSQUARE']:
      list_expr = res.register(self.list_expr())
      if res.error: return res
      return res.success(list_expr)
    
    elif tok.matches(Tokens['KEYWORD'], 'if'):
      if_expr = res.register(self.if_expr(tok.value))
      if res.error: return res
      return res.success(if_expr)

    elif tok.matches(Tokens['KEYWORD'], 'for'):
      for_expr = res.register(self.for_expr(tok.value))
      if res.error: return res
      return res.success(for_expr)

    elif tok.matches(Tokens['KEYWORD'], 'while'):
      while_expr = res.register(self.while_expr(tok.value))
      if res.error: return res
      return res.success(while_expr)

    elif tok.matches(Tokens['KEYWORD'], 'මෙහි'):
      if_expr = res.register(self.if_expr(tok.value))
      if res.error: return res
      return res.success(if_expr)

    elif tok.matches(Tokens['KEYWORD'], 'function') or tok.matches(Tokens['KEYWORD'], 'ශ්‍රීතය') or tok.matches(Tokens['KEYWORD'], 'කාර්යය'):
      func_def = res.register(self.func_def())
      if res.error: return res
      return res.success(func_def)

    return res.failure(InvalidSyntaxError(
      tok.pos_start, tok.pos_end,
      "Expected int, float, identifier, '+', '-', '(', '[', IF', 'FOR', 'WHILE', 'FUN'"
    ))

  def list_expr(self):
    res = ParseResult()
    element_nodes = []
    pos_start = self.current_tok.pos_start.copy()

    if self.current_tok.type != Tokens['LSQUARE']:
      return res.failure(InvalidSyntaxError(
        self.current_tok.pos_start, self.current_tok.pos_end,
        f"Expected '['"
      ))

    res.register_advancement()
    self.advance()

    if self.current_tok.type == Tokens['RSQUARE']:
      res.register_advancement()
      self.advance()
    else:
      element_nodes.append(res.register(self.expr()))
      if res.error:
        return res.failure(InvalidSyntaxError(
          self.current_tok.pos_start, self.current_tok.pos_end,
          "Expected ']', 'VAR', 'IF', 'FOR', 'WHILE', 'FUN', int, float, identifier, '+', '-', '(', '[' or 'NOT'"
        ))

      while self.current_tok.type == Tokens['COMMA']:
        res.register_advancement()
        self.advance()

        element_nodes.append(res.register(self.expr()))
        if res.error: return res

      if self.current_tok.type != Tokens['RSQUARE']:
        return res.failure(InvalidSyntaxError(
          self.current_tok.pos_start, self.current_tok.pos_end,
          f"Expected ',' or ']'"
        ))

      res.register_advancement()
      self.advance()

    return res.success(ListNode(
      element_nodes,
      pos_start,
      self.current_tok.pos_end.copy()
    ))

  def if_expr(self, case_keyword):
    res = ParseResult()
    selected_expr = self.if_expr_cases(case_keyword)
    if selected_expr == "while":
      while_expr = res.register(self.while_expr(case_keyword))
      if res.error: return res
      return res.success(while_expr)
    elif selected_expr == "for":
      for_expr = res.register(self.for_expr(case_keyword))
      if res.error: return res
      return res.success(for_expr)
    else:
      all_cases = res.register(selected_expr)
      if res.error: return res
      cases, else_case = all_cases
      return res.success(IfNode(cases, else_case))

  def if_expr_b(self, case_keyword):
    return self.if_expr_cases(case_keyword)
    
  def if_expr_c(self):
    res = ParseResult()
    else_case = None

    if (self.current_tok.matches(Tokens['KEYWORD'], 'else') or 
        self.current_tok.matches(Tokens['KEYWORD'], 'එසේ_නැත්නම්') or
        self.current_tok.matches(Tokens['KEYWORD'], 'එසේ_නැතිනම්') or
        self.current_tok.matches(Tokens['KEYWORD'], 'එසේත්_නැත්නම්') or
        self.current_tok.matches(Tokens['KEYWORD'], 'එසේත්_නැතිනම්')
        ):
      res.register_advancement()
      self.advance()

      if self.current_tok.type == Tokens['NEWLINE']:
        res.register_advancement()
        self.advance()

        statements = res.register(self.statements())
        if res.error: return res
        else_case = (statements, True)

        if (self.current_tok.matches(Tokens['KEYWORD'], 'end') or 
            self.current_tok.matches(Tokens['KEYWORD'], 'අවසන්')
            ):
          res.register_advancement()
          self.advance()
        else:
          return res.failure(InvalidSyntaxError(
            self.current_tok.pos_start, self.current_tok.pos_end,
            "Expected 'END'"
          ))
      else:
        expr = res.register(self.statement())
        if res.error: return res
        else_case = (expr, False)

    return res.success(else_case)

  def if_expr_b_or_c(self):
    res = ParseResult()
    cases, else_case = [], None

    if (self.current_tok.matches(Tokens['KEYWORD'], 'elseif') or 
        self.current_tok.matches(Tokens['KEYWORD'], 'නැත්නම්') or
        self.current_tok.matches(Tokens['KEYWORD'], 'නැතිනම්')
        ):
      all_cases = res.register(self.if_expr_b(self.current_tok.value))
      if res.error: return res
      cases, else_case = all_cases
    else:
      else_case = res.register(self.if_expr_c())
      if res.error: return res
    
    return res.success((cases, else_case))

  def if_expr_cases(self, case_keyword):
    res = ParseResult()
    cases = []
    else_case = None

    if not self.current_tok.matches(Tokens['KEYWORD'], case_keyword):
      return res.failure(InvalidSyntaxError(
        self.current_tok.pos_start, self.current_tok.pos_end,
        f"Expected '{case_keyword}'"
      ))

    res.register_advancement()
    self.advance()

    tokcopy = self.current_tok.type
    tokvaluecopy = self.current_tok.value

    if self.current_tok.type == Tokens['ID']:
      self.advance()
      if self.current_tok.type == Tokens['EQ']:
        self.advance()
        self.expr()
        if (self.current_tok.matches(Tokens['KEYWORD'], 'to') or
            self.current_tok.matches(Tokens['KEYWORD'], 'සිට​')):
            while not self.current_tok.matches(Tokens['KEYWORD'], 'මෙහි'):
              self.reverse()
            return 'for'
        else:
          while not self.current_tok.matches(Tokens[tokcopy], tokvaluecopy):
            self.reverse()
      else:
        self.reverse()
    else:
      pass

    condition = res.register(self.expr())

    if (self.current_tok.matches(Tokens['KEYWORD'], 'අතරතුර​') or
        self.current_tok.matches(Tokens['KEYWORD'], 'අතර') or
        self.current_tok.matches(Tokens['KEYWORD'], 'do')):
      while not self.current_tok.matches(Tokens['KEYWORD'], 'මෙහි'):
        self.reverse()
      return "while"
    

    if res.error: return res

    if not (self.current_tok.matches(Tokens['KEYWORD'], 'නම්') or 
            self.current_tok.matches(Tokens['KEYWORD'], 'then')
            ):
      return res.failure(InvalidSyntaxError(
        self.current_tok.pos_start, self.current_tok.pos_end,
        f"Expected 'THEN' or 'නම්"
      ))

    res.register_advancement()
    self.advance()


    if self.current_tok.type == Tokens['NEWLINE']:
      res.register_advancement()
      self.advance()


      statements = res.register(self.statements())
      if res.error: return res
      cases.append((condition, statements, True))

      if (self.current_tok.matches(Tokens['KEYWORD'], 'end') or 
          self.current_tok.matches(Tokens['KEYWORD'], 'අවසන්')):
        
        res.register_advancement()
        self.advance()
      else:
        all_cases = res.register(self.if_expr_b_or_c())
        if res.error: return res
        new_cases, else_case = all_cases
        cases.extend(new_cases)
    else:

      expr = res.register(self.statement())
      if res.error: return res
      cases.append((condition, expr, False))

      all_cases = res.register(self.if_expr_b_or_c())
      if res.error: return res
      new_cases, else_case = all_cases
      cases.extend(new_cases)

    return res.success((cases, else_case))

  def for_expr(self, case_keyword):
    res = ParseResult()

    if not self.current_tok.matches(Tokens['KEYWORD'], case_keyword):
      return res.failure(InvalidSyntaxError(
        self.current_tok.pos_start, self.current_tok.pos_end,
        f"Expected '{case_keyword}'"
      ))

    res.register_advancement()
    self.advance()

    if self.current_tok.type != Tokens['ID']:
      return res.failure(InvalidSyntaxError(
        self.current_tok.pos_start, self.current_tok.pos_end,
        f"Expected identifier"
      ))

    var_name = self.current_tok
    res.register_advancement()
    self.advance()

    if self.current_tok.type != Tokens['EQ']:
      return res.failure(InvalidSyntaxError(
        self.current_tok.pos_start, self.current_tok.pos_end,
        f"Expected '='"
      ))
    
    res.register_advancement()
    self.advance()

    start_value = res.register(self.expr())
    if res.error: return res

    if not (self.current_tok.matches(Tokens['KEYWORD'], 'to') or
            self.current_tok.matches(Tokens['KEYWORD'], 'සිට​')):
      return res.failure(InvalidSyntaxError(
        self.current_tok.pos_start, self.current_tok.pos_end,
        f"Expected 'to' or 'සිට​'"
      ))
    
    res.register_advancement()
    self.advance()

    end_value = res.register(self.expr())
    if res.error: return res

    if (self.current_tok.matches(Tokens['KEYWORD'], 'step') or
        self.current_tok.matches(Tokens['KEYWORD'], 'පියවර')):
      res.register_advancement()
      self.advance()

      step_value = res.register(self.expr())
      if res.error: return res
    else:
      step_value = None

    if not (self.current_tok.matches(Tokens['KEYWORD'], 'then') or
            self.current_tok.matches(Tokens['KEYWORD'], 'තෙක්') or
            self.current_tok.matches(Tokens['KEYWORD'], 'දක්වා')):
      return res.failure(InvalidSyntaxError(
        self.current_tok.pos_start, self.current_tok.pos_end,
        f"Expected 'then' or 'තෙක්' or 'දක්වා'"
      ))

    res.register_advancement()
    self.advance()

    if self.current_tok.type == Tokens['NEWLINE']:
      res.register_advancement()
      self.advance()

      body = res.register(self.statements())
      if res.error: return res

      if not (self.current_tok.matches(Tokens['KEYWORD'], 'end') or
              self.current_tok.matches(Tokens['KEYWORD'], 'අවසන්')
              ):
        return res.failure(InvalidSyntaxError(
          self.current_tok.pos_start, self.current_tok.pos_end,
          f"Expected 'end' or 'අවසන්'"
        ))

      res.register_advancement()
      self.advance()

      return res.success(ForNode(var_name, start_value, end_value, step_value, body, True))
    
    body = res.register(self.statement())
    if res.error: return res

    return res.success(ForNode(var_name, start_value, end_value, step_value, body, False))

  def while_expr(self, case_keyword):
    res = ParseResult()
    
    if not self.current_tok.matches(Tokens['KEYWORD'], case_keyword):
      return res.failure(InvalidSyntaxError(
        self.current_tok.pos_start, self.current_tok.pos_end,
        f"Expected '{case_keyword}'"
      ))

    res.register_advancement()
    self.advance()
    
    condition = res.register(self.expr())
    if res.error: return res

    if not (self.current_tok.matches(Tokens['KEYWORD'], 'do') or
            self.current_tok.matches(Tokens['KEYWORD'], 'අතර​') or
            self.current_tok.matches(Tokens['KEYWORD'], 'අතරතුර​')):
      return res.failure(InvalidSyntaxError(
        self.current_tok.pos_start, self.current_tok.pos_end,
        f"Expected 'do'"
      ))

    res.register_advancement()
    self.advance()



    if self.current_tok.type == Tokens['NEWLINE']:
      res.register_advancement()
      self.advance()

      body = res.register(self.statements())
      if res.error: return res

      if not (self.current_tok.matches(Tokens['KEYWORD'], 'end') or 
              self.current_tok.matches(Tokens['KEYWORD'], 'අවසන්')
              ):

        return res.failure(InvalidSyntaxError(
          self.current_tok.pos_start, self.current_tok.pos_end,
          f"Expected 'end' or 'අවසන්'"
        ))

      res.register_advancement()
      self.advance()

      return res.success(WhileNode(condition, body, True))
    
    body = res.register(self.statement())
    if res.error: return res

    return res.success(WhileNode(condition, body, False))

  def func_def(self):
    res = ParseResult()

    if not (self.current_tok.matches(Tokens['KEYWORD'], 'function') or
            self.current_tok.matches(Tokens['KEYWORD'], 'ශ්‍රීතය')):
      return res.failure(InvalidSyntaxError(
        self.current_tok.pos_start, self.current_tok.pos_end,
        f"Expected 'function'"
      ))

    res.register_advancement()
    self.advance()

    if self.current_tok.type == Tokens['ID']:
      var_name_tok = self.current_tok
      res.register_advancement()
      self.advance()
      if self.current_tok.type != Tokens['LPAREN']:
        return res.failure(InvalidSyntaxError(
          self.current_tok.pos_start, self.current_tok.pos_end,
          f"Expected '('"
        ))
    else:
      var_name_tok = None
      if self.current_tok.type != Tokens['LPAREN']:
        return res.failure(InvalidSyntaxError(
          self.current_tok.pos_start, self.current_tok.pos_end,
          f"Expected identifier or '('"
        ))
    
    res.register_advancement()
    self.advance()
    arg_name_toks = []

    if self.current_tok.type == Tokens['ID']:
      arg_name_toks.append(self.current_tok)
      res.register_advancement()
      self.advance()
      
      while self.current_tok.type == Tokens['COMMA']:
        res.register_advancement()
        self.advance()

        if self.current_tok.type != Tokens['ID']:
          return res.failure(InvalidSyntaxError(
            self.current_tok.pos_start, self.current_tok.pos_end,
            f"Expected identifier"
          ))

        arg_name_toks.append(self.current_tok)
        res.register_advancement()
        self.advance()
      
      if self.current_tok.type != Tokens['RPAREN']:
        return res.failure(InvalidSyntaxError(
          self.current_tok.pos_start, self.current_tok.pos_end,
          f"Expected ',' or ')'"
        ))
    else:
      if self.current_tok.type != Tokens['RPAREN']:
        return res.failure(InvalidSyntaxError(
          self.current_tok.pos_start, self.current_tok.pos_end,
          f"Expected identifier or ')'"
        ))

    res.register_advancement()
    self.advance()

    if self.current_tok.type == Tokens['ARROW']:
      res.register_advancement()
      self.advance()

      body = res.register(self.expr())
      if res.error: return res

      return res.success(FuncDefNode(
        var_name_tok,
        arg_name_toks,
        body,
        True
      ))
    
    if self.current_tok.type != Tokens['NEWLINE']:
      return res.failure(InvalidSyntaxError(
        self.current_tok.pos_start, self.current_tok.pos_end,
        f"Expected '->' or NEWLINE"
      ))

    res.register_advancement()
    self.advance()

    body = res.register(self.statements())
    if res.error: return res

    if not (self.current_tok.matches(Tokens['KEYWORD'], 'end') or 
            self.current_tok.matches(Tokens['KEYWORD'], 'අවසන්')
            ):

      return res.failure(InvalidSyntaxError(
        self.current_tok.pos_start, self.current_tok.pos_end,
        f"Expected 'END'"
      ))

    res.register_advancement()
    self.advance()
    
    return res.success(FuncDefNode(
      var_name_tok,
      arg_name_toks,
      body,
      False
    ))

  ###################################

  def bin_op(self, func_a, ops, func_b=None):
    if func_b == None:
      func_b = func_a
    
    res = ParseResult()
    left = res.register(func_a())
    if res.error: return res

    while self.current_tok.type in ops or (self.current_tok.type, self.current_tok.value) in ops:
      op_tok = self.current_tok
      res.register_advancement()
      self.advance()
      right = res.register(func_b())
      if res.error: return res
      left = BinOpNode(left, op_tok, right)

    return res.success(left)
