from src.awk_vm.token import TokenType, Token

JIT = False
if JIT:
  from rpython.rlib.jit import JitDriver
  def jitpolicy(driver):
      from rpython.jit.codewriter.policy import JitPolicy
      return JitPolicy()

  def get_location(skip_next):
    return "@@@@@@@@@@@@@@@@: %s" % (str(skip_next))


  jitdriver = JitDriver(greens=['i', 'skip_next', 'tk', 'tokens', 'heap'], reds=[])#, get_printable_location=get_location)

def condition_eval(tokens, heap):
  lhs = []
  rhs = []
  # comp = Token(None, None)
  comp_token = ''
  for i, tk in enumerate(tokens):
    # TODO: add support for ==, !=, <=, >=
    if tk.token == TokenType.LessThan or tk.token == TokenType.GreaterThan:
      comp_token = str(tk.token)
      lhs = tokens[:i]
      rhs = tokens[i+1:]

  lhs_val = get_token_literal_value(lhs[0].token, lhs[0].value, lhs[0].prop,  lhs, heap, 0)
  rhs_val = get_token_literal_value(rhs[0].token, rhs[0].value, rhs[0].prop,  rhs, heap, 0)
  # lhs_val = get_value(lhs, heap)
  # rhs_val = get_value(rhs, heap)
  
  if comp_token == TokenType.LessThan:
    return lhs_val < rhs_val
  if comp_token == TokenType.GreaterThan:
    return lhs_val > rhs_val
  return False

# heap={}
# tokens=[]

def evaluate_program(tokens, heap=None): 
  skip_next = 0
  if heap == None:
    heap = {}
  for i, tk in enumerate(tokens):
    if JIT:
      jitdriver.jit_merge_point(i=i, skip_next=skip_next, tk=tk, tokens=tokens, heap=heap)
    if skip_next > 0:
      skip_next -= 1
      continue
    if tk.token == TokenType.NewObject:
      heap[tk.value] = {}
    if tk.token == TokenType.Equal and tokens[i-1].token == TokenType.Dot:
      next = tokens[i+1]
      value = get_token_literal_value(next.token, next.value, next.prop,  tokens, heap, i+1)
      heap[tokens[i-1].value][tokens[i-1].prop] = value
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
      while condition_eval(condition_tokens, heap):
        evaluate_program(body_tokens, heap)
      skip_next = cond_i + body_i
      continue
  return heap

def get_token_literal_value(tk_token, tk_value, tk_prop, tokens, heap, i):
  value = 0
  rhs_value = 0

  if tokens[i].token == TokenType.Literal:
    value = tokens[i].numericValue

  if tokens[i].token == TokenType.Dot:
    value = heap[tokens[i].value][tokens[i].prop]

  if i+1 < len(tokens)-1:
    if tokens[i+1].token == TokenType.Plus:
      next = tokens[i+2]
      rhs_value = get_token_literal_value(next.token, next.value, next.prop, tokens, heap, i+2)

  return int(value) + int(rhs_value)

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

# def condition_eval(tokens, objects):
#   lhs = []
#   rhs = []
#   comp_token = ''
#   for i, tk in enumerate(tokens):
#     # TODO: add support for ==, !=, <=, >=
#     if tk.token == TokenType.LessThan or tk.token == TokenType.GreaterThan:
#       comp_token = tk.token
#       lhs = tokens[:i]
#       rhs = tokens[i+1:]

#   # lhs_val = 0
#   # rhs_val = 0
#   # lhs_val = get_value(lhs, objects)
#   # rhs_val = get_value(rhs, objects)
  
#   # if comp_token == '<':#TokenType.LessThan:
#   #     # return lhs_val < rhs_val
#   #     return True
#   # if comp_token == '>': #TokenType.GreaterThan:
#   #     return False
#       # return lhs_val > rhs_val
#   return 0 == 0