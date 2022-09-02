from enum import Enum
from posixpath import split
from typing import Literal



class TokenType(Enum):
    NewObjectStart = '{'
    NewObjectEnd = '}'
    Equal = '='
    Plus = '+'
    Dot = '.'
    Identity = '<identity>'
    End = ';'

class Token():
  def __init__(self, token, value):
      self.token = token
      self.value = value


class Object():
    props = {}
    def __init__(self):
        props = {}


objects = {}


def peek(str, i):
  if i >= len(str):
    return None
  return str[i+1]

"""
Rule 1: object names can be only single letter
Rule 1: object attributes can be only single letter
"""
def parse(index, input):
    tokens = []
    skip_next = 0
    for i, ch in enumerate(input):
        if ch != ' ':
          if skip_next != 0:
              skip_next -= 1
              continue
          if ch == TokenType.Equal.value:
              tokens.append(Token(TokenType.Equal, ""))
              continue
          if ch == TokenType.Dot.value:
              prop = peek(input, i)
              if prop != None:  
                tokens.append(Token(TokenType.Dot, prop))
                continue
          if ch == TokenType.Plus.value:
              tokens.append(Token(TokenType.Plus, prop))
              continue
          if ch == TokenType.End.value:
              tokens.append(Token(TokenType.End, ""))
              continue
          if ch == TokenType.NewObjectEnd.value:
              if tokens[-1].token != TokenType.NewObjectStart:
                raise Exception("syntax error, expected closing new object declaration!")
              continue
          if ch == TokenType.NewObjectStart.value:
              close = peek(input, i)
              if close == TokenType.NewObjectEnd.value:
                tokens.append(Token(TokenType.NewObjectStart, ""))
                skip_next = 1
          else:
            token = peek(input, i)
            if token == TokenType.Dot.value:
                prop = peek(input, i+1)
                if prop != None:  
                  tokens.append(Token(TokenType.Dot, prop))
                  skip_next = 2
            else:
              tokens.append(Token(TokenType.Identity, ch))
    return tokens



src = """
  x = {}
  x.y = 0
  x.y = x.y + 1
  x.z = 2
"""

if __name__ == "__main__":
  i = 0
  for line in src.split('\n'):
    if line != "":
      i += 1
      parse(i, line)
  

