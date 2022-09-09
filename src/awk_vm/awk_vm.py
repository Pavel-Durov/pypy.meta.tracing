import os
from sys import argv
from parser import parse
from program import eval

# dict stringify might cause AttributeError: OrderedDictRepr instance has no attribute ll_str
def print_heap(heap):
  os.write(1, bytes('Awkward heap:\n'))
  for key in heap:
    os.write(1, bytes(key))
    os.write(1, bytes(' : '))
    obj = heap[key]
    os.write(1, bytes('{'))
    for obj_key in obj:
      os.write(1, bytes(' '))
      os.write(1, bytes(obj_key))
      os.write(1, bytes(' : '))
      os.write(1, bytes(obj[obj_key]))
      os.write(1, bytes(', '))
    os.write(1, bytes('}'))
    os.write(1, bytes('\n'))

def run(fp):
    program_contents = ''
    while True:
        read = os.read(fp, 4096)
        if len(read) == 0:
            break
        program_contents += read
    tokens = parse(program_contents)
    heap = eval(tokens, {})
    print_heap(heap)
    


def target(*args):
    return entry_point, None

def entry_point(argv):
    import os
    try:
        filename = argv[1]
    except IndexError:
        print ('You must supply a filename')
        return 1

    run(os.open(filename, os.O_RDONLY, 777))
    return 0


if __name__ == '__main__':
    entry_point(argv)


