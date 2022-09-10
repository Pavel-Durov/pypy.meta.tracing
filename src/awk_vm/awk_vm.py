import os
from sys import argv
from awk_log import trace, print_dict, print_list
from parser import parse
from program import eval


def run(fp):
  trace('run(fp)')
  program_contents = ''
  while True:
      read = os.read(fp, 4096)
      if len(read) == 0:
          break
      program_contents += read
  os.close(fp)
  tokens = parse(program_contents)
  print_list('program', tokens)
  heap = eval(tokens, {})
  print_dict('final heap', heap)


def target(*args):
    trace('target')
    """
    "target" returns the entry point. 
    The translation process imports your module and looks for that name,
    calls it, and the function object returned is where it starts the translation.
    """
    return entry_point, None

def entry_point(argv):
  trace('entry_point(argv)')
  import os
  try:
      filename = argv[1]
  except IndexError:
      print ('You must supply a filename')
      return 1
  run(os.open(filename, os.O_RDONLY, 777))
  return 0


if __name__ == '__main__':
  trace('__main__)')
  entry_point(argv)


