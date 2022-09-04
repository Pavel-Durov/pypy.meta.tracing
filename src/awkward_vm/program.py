from audioop import reverse
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
    for i, tk in enumerate(self.tokens):
      if tk.token.value == TokenType.NewObject.value:
        identity_token = self.tokens[i -2]
        self.objects[identity_token.value] = Object()

      if tk.token.value == TokenType.Plus.value:
        value = self.get_rhs_value(i+1)

      if tk.token.value == TokenType.Dot.value:
        next_token = self.tokens[i+1]
        if next_token.token.value == TokenType.Equal.value:
          value = self.get_rhs_value(i+2)
          obj_key = self.tokens[i-1].value
          self.objects[obj_key].props[tk.value] = value
        
    return self.objects

  def get_rhs_value(self, i):
    value = None
    tk = self.tokens[i]
    next_tk = self.tokens[i+1]
    try:
      value = int(tk.value, base=10)
    except Exception:
      pass

    if type(value) == int:
      if next_tk.token.value == TokenType.Plus.value:
        value = value + self.get_rhs_value(i+2)
    else:
      if tk.token.value == TokenType.Identity.value:
        if next_tk.token.value == TokenType.Dot.value:
          obj_ref = tk.value
          prop_ref = next_tk.value
          value = self.objects[obj_ref].props[prop_ref]
    if (i + 2) < len(self.tokens) - 1 and self.tokens[i+2].token.value == TokenType.Plus.value:
      value = value + self.get_rhs_value(i+3)
    return value
