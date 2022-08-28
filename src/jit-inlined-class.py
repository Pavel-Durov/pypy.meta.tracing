import os

from rpython.rlib.jit import JitDriver, purefunction
from rpython.jit.codewriter.policy import JitPolicy

def jitpolicy(driver):
    return JitPolicy()

def get_location(pc, position, program, bracket_map):
    return "%s_%s_%s" % (program[:pc], program[pc], program[pc + 1:])


jitdriver = JitDriver(greens=['pc', 'position', 'program', 'bracket_map'], reds=['tape'],
                      get_printable_location=get_location)
OPTIMIZED_BRACKET_MAP=True


@purefunction
def get_matching_bracket(bracket_map, pc):
    return bracket_map[pc]

def mainloop(program, bracket_map):
    tape = [0]
    position = 0
    pc = 0

    while pc < len(program):
        # jitdriver.jit_merge_point(pc=pc, position=position, program=program, bracket_map=bracket_map, tape=tape)
        jitdriver.jit_merge_point(pc=pc, tape=tape, program=program, bracket_map=bracket_map, position=position)
        code = program[pc]
        if code == ">":
            position += 1
            if len(tape) <= position:
                tape.append(0)
        elif code == "<":
            position -= 1
        elif code == "+":
            tape[position] += 1
        elif code == "-":
            tape[position] -= 1
        elif code == ".":
            os.write(1, chr(tape[position]))
        elif code == ",":
            tape[position] = ord(os.read(0, 1)[0])
        elif code == "[" and tape[position] == 0:
            pc = get_matching_bracket(bracket_map, pc)
        elif code == "]" and tape[position]!= 0:
            pc = get_matching_bracket(bracket_map, pc)

        pc += 1

def parse(program):
    parsed = []
    bracket_map = {}
    leftstack = []

    pc = 0
    for char in program:
        if char in ('[', ']', '<', '>', '+', '-', ',', '.'):
            parsed.append(char)

            if char == '[':
                leftstack.append(pc)
            elif char == ']':
                left = leftstack.pop()
                right = pc
                bracket_map[left] = right
                bracket_map[right] = left
            pc += 1

    return "".join(parsed), bracket_map



def run(input):
    program, map = parse(input.read())
    mainloop(program, map)


def run(fp):
    program_contents = ""
    while True:
        read = os.read(fp, 4096)
        if len(read) == 0:
            break
        program_contents += read
    os.close(fp)
    program, bm = parse(program_contents)
    mainloop(program, bm)


def entry_point(argv):
    import os
    try:
        filename = argv[1]
    except IndexError:
        print ("You must supply a filename")
        return 1

    run(os.open(filename, os.O_RDONLY, 0777))
    return 0


def target(*args):
    """
  "target" returns the entry point. 
  The translation process imports your module and looks for that name,
  calls it, and the function object returned is where it starts the translation.
  """
    return entry_point, None


if __name__ == "__main__":
    import sys

    entry_point(sys.argv)
