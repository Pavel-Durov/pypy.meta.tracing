class TokenType():
    NewObject = 'new'
    Equal = '='
    LessThan = '<'
    GreaterThan = '>'
    Plus = '+'
    Dot = '.'
    Identity = 'id'
    Literal = 'literal'
    End = ';'
    While = 'while'
    BodyStart = 'body-start'
    BodyEnd = 'body-end'
    Condition = 'cond'


class Token():  
  token = ''
  value = ''
  numericValue = 0
  prop = ''
  def __init__(self, token, literalValue, prop = '', numericValue=0):
      self.token = token
      self.value = literalValue
      self.prop = prop
      self.numericValue = numericValue


  def __str__(self):
     return 'Token: ' + self.token + ' Value: ' + self.value
