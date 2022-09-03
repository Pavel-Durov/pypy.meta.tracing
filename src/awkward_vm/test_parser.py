from src.awkward_vm.parser import clean_input, parse, TokenType


def test_new_object():
    p = parse("x = {};")
    
    assert len(p.tokens) == 4

    assert p.tokens[0].token.value == TokenType.Identity.value
    assert p.tokens[0].value == 'x'
    
    assert p.tokens[1].token.value == TokenType.Equal.value
    assert p.tokens[1].value == ''

    assert p.tokens[2].token.value == TokenType.NewObjectStart.value
    assert p.tokens[2].value == ''

    assert p.tokens[3].token.value == TokenType.End.value
    assert p.tokens[3].value == ''



def test_new_object_with_attribute_set():
    p = parse("x = {}; x.y = 2;")
    assert len(p.tokens) == 9
    assert p.tokens[0].token.value == TokenType.Identity.value
    assert p.tokens[0].value == 'x'
    
    assert p.tokens[1].token.value == TokenType.Equal.value
    assert p.tokens[1].value == ''

    assert p.tokens[2].token.value == TokenType.NewObjectStart.value
    assert p.tokens[2].value == ''

    assert p.tokens[3].token.value == TokenType.End.value
    assert p.tokens[3].value == ''

    assert p.tokens[4].token.value == TokenType.Identity.value
    assert p.tokens[4].value == 'x'

    assert p.tokens[5].token.value == TokenType.Dot.value
    assert p.tokens[5].value == 'y'

    assert p.tokens[6].token.value == TokenType.Equal.value
    assert p.tokens[6].value == ''

    assert p.tokens[7].token.value == TokenType.Identity.value
    assert p.tokens[7].value == '2'

    assert p.tokens[8].token.value == TokenType.End.value
    assert p.tokens[8].value == ''
    

def test_new_object_with_attribute_set_reference():
    p = parse("x.y = x.y + 9;")
    assert len(p.tokens) == 8
    assert p.tokens[0].token.value == TokenType.Identity.value
    assert p.tokens[0].value == 'x'
    
    assert p.tokens[1].token.value == TokenType.Dot.value
    assert p.tokens[1].value == 'y'

    assert p.tokens[2].token.value == TokenType.Equal.value
    assert p.tokens[2].value == ''

    assert p.tokens[3].token.value == TokenType.Identity.value
    assert p.tokens[3].value == 'x'

    assert p.tokens[4].token.value == TokenType.Dot.value
    assert p.tokens[4].value == 'y'

    assert p.tokens[5].token.value == TokenType.Plus.value
    assert p.tokens[5].value == ''

    assert p.tokens[6].token.value == TokenType.Identity.value
    assert p.tokens[6].value == '9'

    assert p.tokens[7].token.value == TokenType.End.value
    assert p.tokens[7].value == ''
    
    
def test_multi_line():
    src = """
      x = {};
      x.y = 0;
      x.y = x.y + 1;
      x.z = 2;
    """
    p = parse(src)
    assert len(p.tokens) == 22


def test_clean_input():
    
    cleaned = clean_input( """
      x = {};
      x.y = 0;
      x.y = x.y + 1;
      x.z = 2;
    """)

    assert cleaned == 'x={};x.y=0;x.y=x.y+1;x.z=2;'
