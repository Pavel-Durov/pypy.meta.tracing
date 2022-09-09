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

    assert tokens[0].token == TokenType.While
    assert tokens[0].value == ''
    
    assert tokens[1].token == TokenType.Dot
    assert tokens[1].value == 'x'
    assert tokens[1].prop == 'y'

    assert tokens[2].token == TokenType.LessThan
    assert tokens[2].value == ''

    assert tokens[3].token == TokenType.Literal
    assert tokens[3].value == '2'

    assert tokens[4].token == TokenType.BodyStart
    assert tokens[4].value == ''

    assert tokens[5].token == TokenType.Dot
    assert tokens[5].value == 'x'
    assert tokens[5].prop == 'y'

    assert tokens[6].token == TokenType.Equal
    assert tokens[6].value == ''

    assert tokens[7].token == TokenType.Dot
    assert tokens[7].value == 'x'
    assert tokens[7].prop == 'y'

    assert tokens[8].token == TokenType.Plus
    assert tokens[8].value == ''

    assert tokens[9].token == TokenType.Literal
    assert tokens[9].value == '1'

    assert tokens[10].token == TokenType.End
    assert tokens[10].value == ''

    assert tokens[11].token == TokenType.BodyEnd
    assert tokens[11].value == ''
