
from src.awkward_vm.program import Program
from src.awkward_vm.token import TokenType, Token

def peek(str, i):
  if i >= len(str):
    return None
  return str[i+1]


def clean_input(str):
  return str.replace('\n', '').replace(' ', '')

"""
Rule 1: object names can be only single letter
Rule 1: object attributes can be only single letter
Rule 2: for now we can only use single value integers
"""
def parse(input):
    input = clean_input(input)
    p = Program(input)
    skip_next = 0
    for i, ch in enumerate(input):
        if skip_next != 0:
            skip_next -= 1
            continue
        if ch == TokenType.Equal.value:
            p.add_token(Token(TokenType.Equal, ""))
            continue
        if ch == TokenType.Dot.value:
            prop = peek(input, i)
            if prop != None:  
              p.add_token(Token(TokenType.Dot, prop))
              continue
        if ch == TokenType.Plus.value:
            p.add_token(Token(TokenType.Plus, ''))
            continue
        if ch == TokenType.End.value:
            p.add_token(Token(TokenType.End, ""))
            continue
        if ch == TokenType.NewObjectEnd.value:
            if p.last_token() != TokenType.NewObjectStart:
              raise Exception("syntax error, expected closing new object declaration!")
            continue
        if ch == TokenType.NewObjectStart.value:
            close = peek(input, i)
            if close == TokenType.NewObjectEnd.value:
              p.add_token(Token(TokenType.NewObjectStart, ""))
              skip_next = 1
        else:
          token = peek(input, i)
          if token == TokenType.Dot.value:
              p.add_token(Token(TokenType.Identity, ch))
              prop = peek(input, i+1)
              if prop != None:  
                p.add_token(Token(TokenType.Dot, prop))
                skip_next = 2
          else:
            p.add_token(Token(TokenType.Identity, ch))
    return p


