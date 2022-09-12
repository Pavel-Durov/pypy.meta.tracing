from src.awk_vm.token import TokenType

from rpython.rlib.jit import JitDriver, purefunction, hint
from rpython.jit.codewriter.policy import JitPolicy


def get_location(pc, tokens):
  tk = tokens[pc]
  return "@@@@@@_awk_loc_%s_%s" % (tk.token, tk.value)

def jitpolicy(driver):
    return JitPolicy()

jitdriver = JitDriver(greens=['pc', 'tokens'], reds=['awk_heap'], get_printable_location=get_location)

class Map(object):
  def __init__(self):
    self.attribute_indexes = {}
    self.other_maps = {}

  @purefunction
  def getindex(self, name):
    return self.attribute_indexes.get(name, -1)

  @purefunction
  def new_map_with_additional_attribute(self, name):
    if name not in self.other_maps:
      newmap = Map()
      newmap.attribute_indexes.update(self.attribute_indexes)
      newmap.attribute_indexes[name] = len(self.attribute_indexes)
      self.other_maps[name] = newmap
    return self.other_maps[name]


EMPTY_MAP = Map()

class AWKObject(object):
  def __init__(self, name):
    self.name = name
    self.map = EMPTY_MAP
    self.storage = []

  def get_field(self, name):
    map = hint(self.map, promote=True)
    index = map.getindex(name)
    if index != -1:
      return self.storage[index]
    raise AttributeError(name)

  def set_field(self, name, value):
    map = hint(self.map, promote=True)
    index = map.getindex(name)
    if index != -1:
        self.storage[index] = value
        return
    self.map = map.new_map_with_additional_attribute(name)
    self.storage.append(value)
  
  def __str__(self):
    result = 'AWKObject(%s) fields\n' % self.name
    for key in self.fields:
      result += '  %s: %s' % (key, self.get_field(key))
    result += '\n'
    return result
      

class AWKHeap():
  def __init__(self, heap):
    self.heap = heap

  def new_obj(self, name):
    self.heap[name] = AWKObject(name)

  def get_obj(self, name):
    return self.heap.get(name)

    
def eval(program, awk_heap): 
  pc = 0
  while pc < len(program):
    jitdriver.jit_merge_point(pc=pc, tokens=program, awk_heap=awk_heap)
    if program[pc].token == TokenType.NewObject:
      awk_heap.new_obj(program[pc].value)
    elif program[pc].token == TokenType.Equal and program[pc-1].token == TokenType.Dot:
      name = program[pc-1].value
      obj = awk_heap.get_obj(name)
      if obj is not None:
        value = get_token_literal_value(program, awk_heap, pc+1)
        field = program[pc-1].prop
        obj.set_field(str(field), int(value))
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
    name = tokens[i].value
    obj = awk_heap.get_obj(name)
    field = tokens[i].prop
    value = obj.get_field(field)

  if i+1 < len(tokens)-1 and tokens[i+1].token == TokenType.Plus:
      rhs_value = get_token_literal_value(tokens, awk_heap, i+2)

  return int(value) + int(rhs_value)
