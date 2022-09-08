from src.awk_vm.token import TokenType, Token

def condition_eval(tokens, objects):
  lhs = []
  rhs = []
  comp = Token(None, None)
  for i, tk in enumerate(tokens):
    # TODO: add support for ==, !=, <=, >=
    if tk.token == TokenType.LessThan or tk.token == TokenType.GreaterThan:
      comp = tk
      lhs = tokens[:i]
      rhs = tokens[i+1:]

  lhs_val = 0
  rhs_val = 0
  lhs_val = get_value(lhs, objects)
  rhs_val = get_value(rhs, objects)
  
  if comp.token == TokenType.LessThan:
      return lhs_val < rhs_val
  if comp.token == TokenType.GreaterThan:
      return lhs_val > rhs_val
  return False


def evaluate_program(tokens, objects):
  skip_next = 0
  for i, tk in enumerate(tokens):
    if skip_next != 0:
      skip_next -= 1
      continue
    if tk.token == TokenType.NewObject:
      identity_token = tokens[i -2]
      objects[identity_token.value] = {}

    if tk.token == TokenType.Plus:
      value = get_rhs_value(tokens, objects, i+1)

    if tk.token == TokenType.Dot:
      next_token = tokens[i+1]
      if next_token.token == TokenType.Equal:
        value = get_rhs_value(tokens, objects, i+2)
        obj_key = tokens[i-1].value
        objects[obj_key][tk.value] = value
      
    if tk.token == TokenType.While:
      condition_tokens = []
      cond_i = 0
      for cond_i, cond_tk in enumerate(tokens[i+1:]):
          if cond_tk.token == TokenType.BodyStart:
              break
          condition_tokens.append(cond_tk)
      body_i = 0
      body_tokens = []
      for body_i, body_tk in enumerate(tokens[i+cond_i+1:]):
        body_tokens.append(body_tk)
        if body_tk.token == TokenType.BodyEnd:
          break
      while condition_eval(condition_tokens, objects):
        evaluate_program(body_tokens, objects)
      skip_next = cond_i + body_i
      continue
  return objects


def get_value(tokens, objects):
  tk = Token(None, None)
  tk = tokens[0]
  value = None
  try:
    value = int(tk.value)
  except Exception:
    obj_ref = tk.value
    next_tk = tokens[1]
    value = objects[obj_ref][next_tk.value]
  return int(value)


def get_rhs_value(tokens, objects, i):
  value = 0
  tk = Token(None, None)
  tk = tokens[i]
  next_tk = Token(None, None)
  next_tk = tokens[i+1]
  try:
    value = int(tk.value)
    if next_tk.token == TokenType.Plus:
      rhs_value = get_rhs_value(tokens, objects, i+2)
      return value + rhs_value
  except Exception:
    if next_tk.token == TokenType.Dot:
      obj_ref = tk.value
      prop_ref = next_tk.value
      value = objects[obj_ref][prop_ref]
    if tokens[i+2].token == TokenType.Plus:
      rhs_value = get_rhs_value(tokens, objects, i+3)
      return value + rhs_value
  return value