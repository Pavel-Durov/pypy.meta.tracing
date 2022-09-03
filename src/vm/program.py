class Object():
    props = {}
    def __init__(self):
        props = {}




class Program():
  objects = {}

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
