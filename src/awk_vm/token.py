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
  condition = []
  body=[]
  
  def __init__(self, token, literalValue, prop = '', numericValue=0, condition = [], body=[]):
      self.token = token
      self.value = literalValue
      self.prop = prop
      self.numericValue = numericValue
      self.condition = condition
      self.body=body


  def __str__(self):
     return '(Token:[' + self.token + '], Value:[' + self.value +'], Prop:[' + self.prop +'], NumericValue:[' + str(self.numericValue) +'])'
