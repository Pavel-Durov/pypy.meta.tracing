from src.awkward_vm.token import TokenType

class Object():
    def __init__(self):
        self.props = {}


class Program():
  objects = {}
  pc = 0
  
  def __init__(self, program):
    self.tokens = []
    self.program = program

  def add_token(self, token):
    self.tokens.append(token)

  def add_tokens(self, tokens):
    self.tokens = self.tokens + tokens

  def last_token(self):
    return self.tokens[-1]

  def print_ast(self):
    for i in self.tokens:
        print(i.token, i.value)

  def get_lfs(self, i, token):
    while i > 0:
      if self.tokens[i].token.value == token.value:
        return self.tokens[i-1]
      i -= 1
      
  def evaluate(self):
    return evaluate_program(self.tokens, self.objects)


      
def get_value(tokens, objects):
  tk = tokens[0]
  value = None
  try:
    value = int(tk.value, base=10)
  except Exception:
    pass
    
  if type(value) == int:
    return value
  else:
    obj_ref = tk.value
    next_tk = tokens[1]
    value = objects[obj_ref].props[next_tk.value]
  
  return value

def condition_eval(tokens, objects):
  lhs = []
  rhs = []
  comp = None
  for i, tk in enumerate(tokens):
    # TODO: add support for ==, !=, <=, >=
    if tk.token.value == TokenType.LessThan.value or tk.token.value == TokenType.GreaterThan.value:
      comp = tk
      lhs = tokens[:i]
      rhs = tokens[i+1:]
  lhs_val = get_value(lhs, objects)
  rhs_val = get_value(rhs, objects)
  
  if comp.token.value == TokenType.LessThan.value:
      return lhs_val < rhs_val
  if comp.token.value == TokenType.GreaterThan.value:
      return lhs_val > rhs_val


def evaluate_program(tokens, objects):
  skip_next = 0
  for i, tk in enumerate(tokens):
    if skip_next != 0:
      skip_next -= 1
      continue
    if tk.token.value == TokenType.NewObject.value:
      identity_token = tokens[i -2]
      objects[identity_token.value] = Object()

    if tk.token.value == TokenType.Plus.value:
      value = get_rhs_value(tokens, objects, i+1)

    if tk.token.value == TokenType.Dot.value:
      next_token = tokens[i+1]
      if next_token.token.value == TokenType.Equal.value:
        value = get_rhs_value(tokens, objects, i+2)
        obj_key = tokens[i-1].value
        objects[obj_key].props[tk.value] = value
      
    if tk.token.value == TokenType.While.value:
      condition_tokens = []
      cond_i = 0
      for cond_i, cond_tk in enumerate(tokens[i+1:]):
          if cond_tk.token.value == TokenType.BodyStart.value:
              break
          condition_tokens.append(cond_tk)
      body_i = 0
      body_tokens = []
      for body_i, body_tk in enumerate(tokens[i+cond_i+1:]):
        body_tokens.append(body_tk)
        if body_tk.token.value == TokenType.BodyEnd.value:
          break
      while condition_eval(condition_tokens, objects):
       
          
        evaluate_program(body_tokens, objects)
      
      skip_next = cond_i + body_i
      continue
  return objects



def while_body_eval(self, tokens):
  for i, tk in enumerate(tokens):
    i = i

  return tokens



def get_rhs_value(tokens, objects, i):
  value = None
  tk = tokens[i]
  next_tk = tokens[i+1]
  try:
    value = int(tk.value, base=10)
  except Exception:
    pass
  if type(value) == int:
    if next_tk.token.value == TokenType.Plus.value:
      value = value + get_rhs_value(tokens, objects, i+2)
  else:
    if tk.token.value == TokenType.Identity.value:
      if next_tk.token.value == TokenType.Dot.value:
        obj_ref = tk.value
        prop_ref = next_tk.value
        value = objects[obj_ref].props[prop_ref]
  if (i + 2) < len(tokens) - 1 and tokens[i+2].token.value == TokenType.Plus.value:
    value = value + get_rhs_value(tokens, objects, i+3)
  return value
