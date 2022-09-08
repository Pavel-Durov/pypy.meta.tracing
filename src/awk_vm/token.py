class TokenType():
    NewObject = 'new'
    Equal = '='
    LessThan = '<'
    GreaterThan = '>'
    Plus = '+'
    Dot = '.'
    Identity = 'id'
    Literal = 'literal' # TODO: use literal type
    End = ';'
    While = 'while'
    BodyStart = 'body-start'
    BodyEnd = 'body-end'
    Condition = 'cond'


class Token():  
  def __init__(self, token, value):
      self.token = token
      self.value = value


  def __str__(self):
     return "Token: " + self.token + " Value: " + self.value
