from src.awk_vm.token import TokenType

from rpython.rlib.jit import JitDriver
from rpython.jit.codewriter.policy import JitPolicy


def get_location(pc, tokens):
  tk = tokens[pc]
  return "@@@@@@_awk_loc_%s_%s" % (tk.token, tk.value)

def jitpolicy(driver):
    return JitPolicy()

jitdriver = JitDriver(greens=['pc', 'tokens'], reds=['awk_heap'], get_printable_location=get_location)

class AWKHeap():
  def __init__(self, heap):
      self.objects = heap

  def new_obj(self, name):
      self.objects[name] = {}
  
  def set(self, key, value):
      self.objects[key] = value
  
  def set(self, obj_name, obj_prop, value):
      self.objects[obj_name][obj_prop] = value
  
  def get(self, obj_name, obj_prop):
      return self.objects[obj_name][obj_prop]
    

def eval(program, awk_heap): 
  pc = 0
  while pc < len(program):
    jitdriver.jit_merge_point(pc=pc, tokens=program, awk_heap=awk_heap)
    if program[pc].token == TokenType.NewObject:
      awk_heap.new_obj(program[pc].value)

    elif program[pc].token == TokenType.Equal and program[pc-1].token == TokenType.Dot:
      obj_name = program[pc-1].value
      obj_prop = program[pc-1].prop
      value = get_token_literal_value(program, awk_heap, pc+1)
      awk_heap.set(obj_name, obj_prop, value)

    elif program[pc].token == TokenType.While:
      while condition_eval(program[pc].condition, awk_heap):
        eval(program[pc].body, awk_heap)

    pc += 1
  return awk_heap

def condition_eval(tokens, awk_heap):
  for i, tk in enumerate(tokens):
    # TODO: add support for ==, !=, <=, >=
    if tk.token == TokenType.LessThan or tk.token == TokenType.GreaterThan:
      lhs_val = get_token_literal_value(tokens[:i], awk_heap, 0)
      rhs_val = get_token_literal_value(tokens[i+1:], awk_heap, 0)

      if tk.token == TokenType.LessThan:
        return lhs_val < rhs_val
      if tk.token == TokenType.GreaterThan:
        return lhs_val > rhs_val
      else:
        break
  return False

def get_token_literal_value(tokens, awk_heap, i):
  value = 0
  rhs_value = 0

  if tokens[i].token == TokenType.Literal:
    value = tokens[i].numericValue

  if tokens[i].token == TokenType.Dot:
    value = awk_heap.get(tokens[i].value, tokens[i].prop)

  if i+1 < len(tokens)-1 and tokens[i+1].token == TokenType.Plus:
      rhs_value = get_token_literal_value(tokens, awk_heap, i+2)

  return value + rhs_value
