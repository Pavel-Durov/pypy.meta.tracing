import os
from parser import parse

src = """
  x = {};
  x.y = 0;
  x.y = x.y + 1;
  x.z = 2;
"""


def run(fp):
    program_contents = ""
    while True:
        read = os.read(fp, 4096)
        if len(read) == 0:
            break
        program_contents += read
    program_ = parse(program_contents)
    program_.evaluate()

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
    import sys

    entry_point(sys.argv)
