from src.awk_vm.token import TokenType, Token

JIT = False

if JIT:
  from rpython.rlib.jit import JitDriver

  def jitpolicy(driver):
      from rpython.jit.codewriter.policy import JitPolicy
      return JitPolicy()

  def get_location(skip_next):
    return "@@@@@@@@@@@@@@@@: %s" % (str(skip_next))


  jitdriver = JitDriver(greens=['JIT', 'pc', 'tokens'], reds=['heap'])#, get_printable_location=get_location)

def evaluate_program(tokens, heap): 
  pc = 0
  while pc < len(tokens):
    if JIT:
      jitdriver.jit_merge_point(JIT=JIT, pc=pc, tokens=tokens, heap=heap)

    if tokens[pc].token == TokenType.NewObject:
      heap[tokens[pc].value] = {}

    elif tokens[pc].token == TokenType.Equal and tokens[pc-1].token == TokenType.Dot:
      heap[tokens[pc-1].value][tokens[pc-1].prop] = get_token_literal_value(tokens, heap, pc+1)

    elif tokens[pc].token == TokenType.While:
      while condition_eval(tokens[pc].condition, heap):
        evaluate_program(tokens[pc].body, heap)

    pc += 1

  return heap

def condition_eval(tokens, heap):
  for i, tk in enumerate(tokens):
    # TODO: add support for ==, !=, <=, >=
    if tk.token == TokenType.LessThan or tk.token == TokenType.GreaterThan:
      lhs_val = get_token_literal_value(tokens[:i], heap, 0)
      rhs_val = get_token_literal_value(tokens[i+1:], heap, 0)

      if tk.token == TokenType.LessThan:
        return lhs_val < rhs_val
      if tk.token == TokenType.GreaterThan:
        return lhs_val > rhs_val
      else:
        break
  return False

def get_token_literal_value(tokens, heap, i):
  value = 0
  rhs_value = 0

  if tokens[i].token == TokenType.Literal:
    value = tokens[i].numericValue

  if tokens[i].token == TokenType.Dot:
    value = heap[tokens[i].value][tokens[i].prop]

  if i+1 < len(tokens)-1:
    if tokens[i+1].token == TokenType.Plus:
      rhs_value = get_token_literal_value(tokens, heap, i+2)

  return int(value) + int(rhs_value)
