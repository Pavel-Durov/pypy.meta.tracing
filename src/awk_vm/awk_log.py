import os

def trace(msg):
  os.write(1, bytes('trace: '))
  os.write(1, bytes(msg))    
  os.write(1, bytes('\n'))
  
def print_dict(msg, dict):
  # TODO: dict stringify might cause AttributeError: OrderedDictRepr instance has no attribute ll_str
  os.write(1, bytes('\n'))
  os.write(1, bytes(msg))
  os.write(1, bytes(': '))
  for key in dict:
    os.write(1, bytes(key))
    os.write(1, bytes(' : '))
    obj = dict[key]
    os.write(1, bytes('{'))
    for obj_key in obj:
      os.write(1, bytes(' '))
      os.write(1, bytes(obj_key))
      os.write(1, bytes(' : '))
      os.write(1, bytes(obj[obj_key]))
      os.write(1, bytes(', '))
    os.write(1, bytes('}, '))
  os.write(1, bytes('\n'))
    

def print_list(msg, list):
  # TODO: dict stringify might cause AttributeError: OrderedDictRepr instance has no attribute ll_str
  os.write(1, bytes(msg))
  os.write(1, bytes('['))
  for item in list:
    os.write(1, bytes(str(item)))
    os.write(1, bytes(','))
  os.write(1, bytes(']'))
  