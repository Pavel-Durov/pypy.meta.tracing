from src.awk_vm.token import TokenType, Token

def peek(str, i):
  if i >= len(str):
    return ''
  return str[i+1]

def clean_input(str):
  # Q: Why not use srt.replace? Cause RPython doesn't support it...
  result = ''
  for char in str:
    if char == '\n' or char == ' ':
      continue
    result = result + char
  return result

def parse(raw_program):
    tokens = []
    prog_in = clean_input(raw_program)
    skip_next = 0
    for i, ch in enumerate(prog_in):
        if skip_next != 0:
            skip_next -= 1
            continue
        if ch == '=':
            tokens.append(Token(TokenType.Equal, ''))
            continue
        if ch == '>':
            tokens.append(Token(TokenType.GreaterThan, ''))
            continue
        if ch == '<':
            tokens.append(Token(TokenType.LessThan, ''))
            continue
        if ch == '+':
            tokens.append(Token(TokenType.Plus, ''))
            continue
        if ch == ';':
            tokens.append(Token(TokenType.End, ''))
            continue
        if ch == '{':
            if prog_in[i+1] == '}':
              id = prog_in[i-2]
              tokens.append(Token(TokenType.NewObject, id))
              skip_next = 1
              continue
        if ch == 'w':
            if prog_in[i:i+len('while')] == 'while':
              skip_next = parse_while_token(prog_in[i:], tokens) -1
            continue
        else:
          if i+1 < len(prog_in) and prog_in[i+1] == '.':
              prop = peek(prog_in, i+1)
              if prop == '':  
                tokens.append(Token(TokenType.Identity, ch))
              else:
                tokens.append(Token(TokenType.Dot, ch, prop))
                skip_next = 2
          else:
            value = get_numeric_value(i, prog_in)
            if value is None:
              tokens.append(Token(TokenType.Identity, ch))
            else:
              tokens.append(Token(TokenType.Literal, value, numericValue=int(value)))
              skip_next = len(value) - 1
              
    return tokens


def parseInt(s):
  try:
    int(s)
    return True
  except Exception:
    return False


def get_numeric_value(prog_i, input):
  result = None
  # Q: Why not use str.isnumeric? Cause RPython doesn't support it...
  if parseInt(input[prog_i]):
    result = ''
    for i in range(prog_i, len(input)):
      if parseInt(input[i]):
        result += input[i]
      else:
        break
  return result
  

def parse_while_token(input, tokens):
  condition_tokens, cond_i = parse_while_condition(input[len('while'):])
  body_tokens, body_i = parse_while_body(input[len('while')+cond_i + 1:])
  tokens.append(Token(TokenType.While, '', condition=condition_tokens, body=body_tokens))
  skip_next = len('while') + cond_i + body_i + 2
  return skip_next

def parse_while_body(input):
  tokens = []
  body = ''
  for body_i, ch in enumerate(input):
    if ch == '{':
      tokens.append(Token(TokenType.BodyStart, ''))
      continue
    if ch == '}':
      tokens = tokens + parse(body)
      tokens.append(Token(TokenType.BodyEnd, ''))
      return tokens, body_i
    body = body + ch
  return tokens, 0
  

def parse_while_condition(input):
  tokens = None
  condition = ''
  for cond_i, ch in enumerate(input):
    if ch == '(':
      continue
    if ch == ')':
      tokens = parse(condition)
      return tokens, cond_i
    condition = condition + ch
  return tokens, 0
  