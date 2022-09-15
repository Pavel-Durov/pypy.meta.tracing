from src.awk_vm.token import TokenType

from rpython.rlib.jit import JitDriver, purefunction, hint
from rpython.jit.codewriter.policy import JitPolicy


def get_location(pc, tokens):
    tk = tokens[pc]
    return "@@@@@@_awk_loc_%s_%s" % (tk.token, tk.value)


def jitpolicy(driver):
    return JitPolicy()


jitdriver = JitDriver(greens=['pc', 'tokens'], reds=[
                      'awk_heap'], get_printable_location=get_location)


@purefunction
def get_opcode(program, pc):
    if pc < len(program):
      return program[pc]
    return None

def eval(program, awk_heap):
    program = hint(program, promote=True)
    pc = 0
    while pc < len(program):
        jitdriver.jit_merge_point(pc=pc, tokens=program, awk_heap=awk_heap)

        if get_opcode(program, pc).token == TokenType.NewObject:
            awk_heap.new_obj(get_opcode(program, pc).value)
        elif get_opcode(program, pc).token == TokenType.Equal and get_opcode(program, pc - 1).token == TokenType.Dot:
            name = get_opcode(program, pc - 1).value
            obj = awk_heap.get_obj(name)
            if obj is not None:
                value = get_token_literal_value(program, awk_heap, pc+1)
                field = get_opcode(program, pc - 1).prop
                obj.set_field(str(field), int(value))
        elif get_opcode(program, pc).token == TokenType.While:
            while condition_eval(get_opcode(program, pc).condition, awk_heap):
                eval(get_opcode(program, pc).body, awk_heap)
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
    
    if get_opcode(tokens, i).token == TokenType.Literal:
        value = get_opcode(tokens, i).numericValue

    if get_opcode(tokens, i).token == TokenType.Dot:
        name = get_opcode(tokens, i).value
        obj = awk_heap.get_obj(name)
        field = get_opcode(tokens, i).prop
        value = obj.get_field(field)
    
    token = get_opcode(tokens, i+1)

    if token is not None and get_opcode(tokens, i+1).token == TokenType.Plus:
        rhs_value = get_token_literal_value(tokens, awk_heap, i+2)

    return int(value) + int(rhs_value)
