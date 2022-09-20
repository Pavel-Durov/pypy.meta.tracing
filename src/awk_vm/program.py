from src.awk_vm.token import TokenType

from rpython.rlib.jit import JitDriver, purefunction, hint
from rpython.jit.codewriter.policy import JitPolicy


def jitpolicy(driver):
    return JitPolicy()


jitdriver = JitDriver(greens=["pc", "tokens"], reds=["awk_heap"])


@purefunction
def get_opcode_numericValue(program, pc):
    if pc < len(program):
        return program[pc].numericValue
    return -1


@purefunction
def get_opcode_token(program, pc):
    if pc < len(program):
        return program[pc].token
    return -1


@purefunction
def get_opcode_value(program, pc):
    if pc < len(program):
        return program[pc].value
    return ""


@purefunction
def get_opcode_prop(program, pc):
    if pc < len(program):
        return program[pc].prop
    return ""


@purefunction
def get_opcode_prop_condition(program, pc):
    if pc < len(program):
        return program[pc].condition
    return None


@purefunction
def get_opcode_prop_body(program, pc):
    if pc < len(program):
        return program[pc].body
    return []


def eval(program, awk_heap):
    program = hint(program, promote=True)
    pc = 0
    while pc < len(program):
        jitdriver.jit_merge_point(pc=pc, tokens=program, awk_heap=awk_heap)

        if get_opcode_token(program, pc) == TokenType.NewObject:
            awk_heap.new_obj(get_opcode_value(program, pc))
        elif (
            get_opcode_token(program, pc) == TokenType.Equal
            and get_opcode_token(program, pc - 1) == TokenType.Dot
        ):
            name = get_opcode_value(program, pc - 1)
            obj = awk_heap.get_obj(name)
            if obj is not None:
                value = get_token_literal_value(program, awk_heap, pc + 1)
                field = get_opcode_prop(program, pc - 1)
                obj.set_field(str(field), int(value))
        elif get_opcode_token(program, pc) == TokenType.While:
            while condition_eval(get_opcode_prop_condition(program, pc), awk_heap):
                eval(get_opcode_prop_body(program, pc), awk_heap)
        pc += 1
    return awk_heap


def condition_eval(tokens, awk_heap):
    for i, tk in enumerate(tokens):
        # TODO: add support for ==, !=, <=, >=
        if tk.token == TokenType.LessThan or tk.token == TokenType.GreaterThan:
            lhs_val = get_token_literal_value(tokens[:i], awk_heap, 0)
            rhs_val = get_token_literal_value(tokens[i + 1 :], awk_heap, 0)
            if tk.token == TokenType.LessThan:
                return lhs_val < rhs_val
            if tk.token == TokenType.GreaterThan:
                return lhs_val > rhs_val
            else:
                break
    return False


def get_token_literal_value(program, awk_heap, i):
    value = 0
    rhs_value = 0

    if get_opcode_token(program, i) == TokenType.Literal:
        value = get_opcode_numericValue(program, i)

    if get_opcode_token(program, i) == TokenType.Dot:
        name = get_opcode_value(program, i)
        obj = awk_heap.get_obj(name)
        field = get_opcode_prop(program, i)
        value = obj.get_field(field)

    token = get_opcode_token(program, i + 1)

    if token == TokenType.Plus:
        rhs_value = get_token_literal_value(program, awk_heap, i + 2)

    return int(value) + int(rhs_value)
