from src.vm.token import TokenType

class Object():
    def __init__(self):
        self.props = {}
    def set(self, name, value):
        self.props[name] = value


class Program():
  objects = {}
  pc = 0
  
  def __init__(self, program):
    self.tokens = []
    self.program = program

  def add_token(self, token):
    self.tokens.append(token)

  def last_token(self):
    return self.tokens[-1]

  def print_ast(self):
    for i in self.tokens:
        print(i.token, i.value)

  def evaluate(self):
    for i, tk in enumerate(self.tokens):
      if tk.token.value == TokenType.NewObjectStart.value:
        identity_token = self.tokens[i -2]
        self.objects[identity_token.value] = Object()
      if tk.token.value == TokenType.Dot.value:
        obj_key = self.tokens[i-1].value
        next_token = self.tokens[i+1]
        value = self.tokens[i+2].value
        if next_token.token.value == TokenType.Equal.value:
          # TODO: parse to int if value is int
          self.objects[obj_key].set(tk.value, value)
    return self.objects