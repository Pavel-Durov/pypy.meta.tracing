import os
from sys import argv
from parser import parse
from program import evaluate_program
from rpython.rlib.jit import JitDriver


def jitpolicy(driver):
    from rpython.jit.codewriter.policy import JitPolicy
    return JitPolicy()

def get_location(heap):
    return "@@@@@@@@@@@@@@@@: %s" % (len(heap))


jitdriver = JitDriver(greens=['tokens'], reds=['heap'], get_printable_location=get_location)

def print_heap(heap):
  os.write(1, bytes("Awkward heap:\n"))
  for key in heap:
    os.write(1, bytes(key))
    # os.write(1, bytes(" : "))
    # os.write(1, bytes(heap[key]))
    os.write(1, bytes("\n"))

def run(fp):
    program_contents = ""
    while True:
        read = os.read(fp, 4096)
        if len(read) == 0:
            break
        program_contents += read
    tokens = parse(program_contents)
    heap = {}
    jitdriver.jit_merge_point(tokens=tokens, heap=heap)
    evaluate_program(tokens, heap)
    print_heap(heap)


def target(*args):
    return entry_point, None

def entry_point(argv):
    import os
    try:
        filename = argv[1]
    except IndexError:
        print ("You must supply a filename")
        return 1

    run(os.open(filename, os.O_RDONLY, 777))
    return 0


if __name__ == "__main__":
    entry_point(argv)


