from src.awk_vm.token import TokenType
from src.awk_vm.parser import clean_input, parse



def test_new_object():
    tokens = parse("x = {};")
    
    assert len(tokens) == 4

    assert tokens[0].token == TokenType.Identity
    assert tokens[0].value == 'x'
    
    assert tokens[1].token == TokenType.Equal
    assert tokens[1].value == ''

    assert tokens[2].token == TokenType.NewObject
    assert tokens[2].value == 'x'

    assert tokens[3].token == TokenType.End
    assert tokens[3].value == ''



def test_new_object_with_attribute_set():
    tokens = parse("x = {}; x.y = 2;")
    
    assert tokens[0].token == TokenType.Identity
    assert tokens[0].value == 'x'
    
    assert tokens[1].token == TokenType.Equal
    assert tokens[1].value == ''

    assert tokens[2].token == TokenType.NewObject
    assert tokens[2].value == 'x'

    assert tokens[3].token == TokenType.End
    assert tokens[3].value == ''

    assert tokens[4].token == TokenType.Dot
    assert tokens[4].value == 'x'
    assert tokens[4].prop == 'y'

    assert tokens[5].token == TokenType.Equal
    assert tokens[5].value == ''

    assert tokens[6].token == TokenType.Literal
    assert tokens[6].value == '2'

    assert tokens[7].token == TokenType.End
    assert tokens[7].value == ''
    
    
def test_multi_line():
    src = """
      x = {};
      x.y = 0;
      x.y = x.y + 1;
      x.z = 2;
    """
    tokens = parse(src)
    assert len(tokens) == 18


def test_clean_input():
    
    cleaned = clean_input( """
      x = {};
      x.y = 0;
      x.y = x.y + 1;
      x.z = 2;
    """)

    assert cleaned == 'x={};x.y=0;x.y=x.y+1;x.z=2;'


def test_while_loop():
    tokens = parse( """
      while (x.y < 2) { 
        x.y = x.y + 1; 
      }
    """)
    while_tk =  tokens[0]
    assert while_tk.token == TokenType.While
    assert while_tk.value == ''
    
    condition = while_tk.condition
    assert condition[0].token == TokenType.Dot
    assert condition[0].value == 'x'
    assert condition[0].prop == 'y'

    assert condition[1].token == TokenType.LessThan
    assert condition[1].value == ''

    assert condition[2].token == TokenType.Literal
    assert condition[2].value == '2'

    body = while_tk.body
    assert body[0].token == TokenType.BodyStart
    assert body[0].value == ''

    assert body[1].token == TokenType.Dot
    assert body[1].value == 'x'
    assert body[1].prop == 'y'

    assert body[2].token == TokenType.Equal
    assert body[2].value == ''

    assert body[3].token == TokenType.Dot
    assert body[3].value == 'x'
    assert body[3].prop == 'y'

    assert body[4].token == TokenType.Plus
    assert body[4].value == ''

    assert body[5].token == TokenType.Literal
    assert body[5].value == '1'

    assert body[6].token == TokenType.End
    assert body[6].value == ''

    assert body[7].token == TokenType.BodyEnd
    assert body[7].value == ''
