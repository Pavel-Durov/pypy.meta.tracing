
from enum import Enum


class TokenType(Enum):
    NewObjectStart = '{'
    NewObjectEnd = '}'
    Equal = '='
    Plus = '+'
    Dot = '.'
    Identity = 'id'
    Literal = 'literal' # TODO: use literal type
    End = ';'

class Token():
  def __init__(self, token, value):
      self.token = token
      self.value = value
  def __str__(self):
     return "Token: " + self.token.value + " Value: " + self.value