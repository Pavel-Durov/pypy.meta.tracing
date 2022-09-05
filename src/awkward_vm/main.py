import os
from sys import argv
from parser import parse

# from rpython.rlib.jit import JitDriver
# from rpython.jit.codewriter.policy import JitPolicy

# def jitpolicy(driver):
#     return JitPolicy()

# def get_location(program):
#     return "%s" % (program.pc)


# jitdriver = JitDriver(greens=['program'], reds=[], get_printable_location=get_location)


def run(fp):
    program_contents = ""
    while True:
        read = os.read(fp, 4096)
        if len(read) == 0:
            break
        program_contents += read
    program = parse(program_contents)
    # jitdriver.jit_merge_point(program=program)
    program.evaluate()


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


