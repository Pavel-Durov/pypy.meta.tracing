from src.awk_vm.token import TokenType, Token
from src.awk_vm.awk_log import trace, print_dict

from rpython.rlib.jit import JitDriver
from rpython.jit.codewriter.policy import JitPolicy


def get_location(pc, tokens):
  tk = tokens[pc]
  return "%s_%s" % (tk.token, tk.value)

def jitpolicy(driver):
    return JitPolicy()

jitdriver = JitDriver(greens=['pc', 'tokens'], reds=['heap'], get_printable_location=get_location)

def eval(program, heap): 
  pc = 0
  while pc < len(program):
    jitdriver.jit_merge_point(pc=pc, tokens=program, heap=heap)
    trace('pc: %s' % pc)
    print_dict('loop heap', heap)
    if program[pc].token == TokenType.NewObject:
      heap[program[pc].value] = {}

    elif program[pc].token == TokenType.Equal and program[pc-1].token == TokenType.Dot:
      heap[program[pc-1].value][program[pc-1].prop] = get_token_literal_value(program, heap, pc+1)

    elif program[pc].token == TokenType.While:
      while condition_eval(program[pc].condition, heap):
        eval(program[pc].body, heap)

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
