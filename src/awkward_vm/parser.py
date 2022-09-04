
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
def parse(raw_program):
    clean_program = clean_input(raw_program)
    p = Program(clean_program)
    skip_next = 0
    for i, ch in enumerate(clean_program):
        if skip_next != 0:
            skip_next -= 1
            continue
        if ch == '=':
            p.add_token(Token(TokenType.Equal, ""))
            continue
        if ch == '>':
            p.add_token(Token(TokenType.GreaterThan, ""))
            continue
        if ch == '<':
            p.add_token(Token(TokenType.LessThan, ""))
            continue
        # if ch == '.':
        #     p.add_token(Token(TokenType.Dot, prop))
        #     continue
        if ch == '+':
            p.add_token(Token(TokenType.Plus, ''))
            continue
        if ch == ';':
            p.add_token(Token(TokenType.End, ""))
            continue
        if ch == '{':
            if clean_program[i+1] == '}':
              p.add_token(Token(TokenType.NewObject, ""))
              skip_next = 1
              continue
        if ch == 'w':
            if clean_program[i:i+len('while')] == 'while':
              skip_next = parse_while_token(i, clean_program[i:], p) -1
            continue
        else:
          if i+1 < len(clean_program) and clean_program[i+1] == '.':
              p.add_token(Token(TokenType.Identity, ch))
              prop = peek(clean_program, i+1)
              if prop != None:  
                p.add_token(Token(TokenType.Dot, prop))
                skip_next = 2
          else:
            # TODO: use literals as tokens
            p.add_token(Token(TokenType.Identity, ch))
    return p

def parse_while_token(i, input, p):
  p.add_token(Token(TokenType.While, ""))
  condition_tokens, cond_i = parse_while_condition(input[len('while'):])
  p.add_tokens(condition_tokens)
  body_tokens, body_i = parse_while_body(input[len('while')+cond_i + 1:])
  p.add_tokens(body_tokens)
  skip_next = len('while') + cond_i + body_i + 2
  return skip_next

def parse_while_body(input):
  tokens = []
  body = ""
  for body_i, ch in enumerate(input):
    if ch == '{':
      tokens.append(Token(TokenType.BodyStart, ""))
      continue
    if ch == '}':
      condition_tokens = parse(body)
      tokens = tokens + condition_tokens.tokens
      tokens.append(Token(TokenType.BodyEnd, ""))
      return tokens, body_i
    body = body + ch
  return tokens, 0
  

def parse_while_condition(input):
  tokens = None
  condition = ""
  for cond_i, ch in enumerate(input):
    if ch == '(':
      continue
    if ch == ')':
      condition_tokens = parse(condition)
      tokens = condition_tokens.tokens
      return tokens, cond_i
    condition = condition + ch
  return tokens, 0
  