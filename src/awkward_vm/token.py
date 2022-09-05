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
  def __init__(self, token, value, body=None):
      self.token = token
      self.value = value
      self.body = body
  def __str__(self):
     return "Token: " + self.token + " Value: " + self.value
