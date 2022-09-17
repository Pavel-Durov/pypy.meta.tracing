import os
from sys import argv
from src.awk_vm.awk_log import print_dict, trace
from src.awk_vm.parser import parse
from src.awk_vm.program import eval
from src.awk_vm.awk_heap import AwkSelfLikeHeap, AwkSimpleHeap

SELF_LIKE_MAPS_OPT = True


def run(fp):
    program_contents = ""
    while True:
        read = os.read(fp, 4096)
        if len(read) == 0:
            break
        program_contents += read
    os.close(fp)
    tokens = parse(program_contents)
    if SELF_LIKE_MAPS_OPT:
        trace("evaluating with self-like heap")
        awk_heap = eval(tokens, AwkSelfLikeHeap({}))
    else:
        trace("evaluating with simple heap")
        awk_heap = eval(tokens, AwkSimpleHeap({}))
    print_dict("awk heap", awk_heap.heap)


def target(*args):
    """
    "target" returns the entry point.
    The translation process imports your module and looks for that name,
    calls it, and the function object returned is where it starts the translation.
    """
    return entry_point, None


def entry_point(argv):
    import os

    try:
        filename = argv[1]
    except IndexError:
        print("You must supply a filename")
        return 1
    run(os.open(filename, os.O_RDONLY, 777))
    return 0


if __name__ == "__main__":
    entry_point(argv)
