from src.awkward_vm.parser import clean_input, parse, TokenType


def test_new_object():
    p = parse("x = {};")
    
    assert len(p.tokens) == 4

    assert p.tokens[0].token == TokenType.Identity
    assert p.tokens[0].value == 'x'
    
    assert p.tokens[1].token == TokenType.Equal
    assert p.tokens[1].value == ''

    assert p.tokens[2].token == TokenType.NewObject
    assert p.tokens[2].value == ''

    assert p.tokens[3].token == TokenType.End
    assert p.tokens[3].value == ''



def test_new_object_with_attribute_set():
    p = parse("x = {}; x.y = 2;")
    assert len(p.tokens) == 9
    assert p.tokens[0].token == TokenType.Identity
    assert p.tokens[0].value == 'x'
    
    assert p.tokens[1].token == TokenType.Equal
    assert p.tokens[1].value == ''

    assert p.tokens[2].token == TokenType.NewObject
    assert p.tokens[2].value == ''

    assert p.tokens[3].token == TokenType.End
    assert p.tokens[3].value == ''

    assert p.tokens[4].token == TokenType.Identity
    assert p.tokens[4].value == 'x'

    assert p.tokens[5].token == TokenType.Dot
    assert p.tokens[5].value == 'y'

    assert p.tokens[6].token == TokenType.Equal
    assert p.tokens[6].value == ''

    assert p.tokens[7].token == TokenType.Identity
    assert p.tokens[7].value == '2'

    assert p.tokens[8].token == TokenType.End
    assert p.tokens[8].value == ''
    

def test_new_object_with_attribute_set_reference():
    p = parse("x.y = x.y + 9;")
    assert len(p.tokens) == 8
    assert p.tokens[0].token == TokenType.Identity
    assert p.tokens[0].value == 'x'
    
    assert p.tokens[1].token == TokenType.Dot
    assert p.tokens[1].value == 'y'

    assert p.tokens[2].token == TokenType.Equal
    assert p.tokens[2].value == ''

    assert p.tokens[3].token == TokenType.Identity
    assert p.tokens[3].value == 'x'

    assert p.tokens[4].token == TokenType.Dot
    assert p.tokens[4].value == 'y'

    assert p.tokens[5].token == TokenType.Plus
    assert p.tokens[5].value == ''

    assert p.tokens[6].token == TokenType.Identity
    assert p.tokens[6].value == '9'

    assert p.tokens[7].token == TokenType.End
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


def test_while_loop():
    p = parse( """
      while (x.y < 2) { 
        x.y = x.y + 1; 
      }
    """)

    assert p.tokens[0].token == TokenType.While
    assert p.tokens[0].value == ''
    
    assert p.tokens[1].token == TokenType.Identity
    assert p.tokens[1].value == 'x'

    assert p.tokens[2].token == TokenType.Dot
    assert p.tokens[2].value == 'y'

    assert p.tokens[3].token == TokenType.LessThan
    assert p.tokens[3].value == ''
    
    assert p.tokens[4].token == TokenType.Identity
    assert p.tokens[4].value == '2'

    assert p.tokens[5].token == TokenType.BodyStart
    assert p.tokens[5].value == ''

    assert p.tokens[6].token == TokenType.Identity
    assert p.tokens[6].value == 'x'

    assert p.tokens[7].token == TokenType.Dot
    assert p.tokens[7].value == 'y'

    assert p.tokens[8].token == TokenType.Equal
    assert p.tokens[8].value == ''

    assert p.tokens[9].token == TokenType.Identity
    assert p.tokens[9].value == 'x'

    assert p.tokens[10].token == TokenType.Dot
    assert p.tokens[10].value == 'y'

    assert p.tokens[11].token == TokenType.Plus
    assert p.tokens[11].value == ''

    assert p.tokens[12].token == TokenType.Identity
    assert p.tokens[12].value == '1'

    assert p.tokens[13].token == TokenType.End
    assert p.tokens[13].value == ''

    assert p.tokens[14].token == TokenType.BodyEnd
    assert p.tokens[14].value == ''
    


def test_while_loop():
    p = parse( """
      x = {};
      x.a = 1;
      while (x.y < 2) { 
       x.a = x.a + 1; 
      }
      x.z = 5;
    """)

    assert p.tokens[0].token == TokenType.Identity
    assert p.tokens[0].value == 'x'
    
    assert p.tokens[1].token == TokenType.Equal
    assert p.tokens[1].value == ''

    assert p.tokens[2].token == TokenType.NewObject
    assert p.tokens[2].value == ''

    assert p.tokens[3].token == TokenType.End
    assert p.tokens[3].value == ''

    assert p.tokens[4].token == TokenType.Identity
    assert p.tokens[4].value == 'x'

    assert p.tokens[5].token == TokenType.Dot
    assert p.tokens[5].value == 'a'

    assert p.tokens[6].token == TokenType.Equal
    assert p.tokens[6].value == ''

    assert p.tokens[7].token == TokenType.Identity
    assert p.tokens[7].value == '1'

    assert p.tokens[8].token == TokenType.End
    assert p.tokens[8].value == ''

    assert p.tokens[9].token == TokenType.While
    assert p.tokens[9].value == ''
    
    assert p.tokens[10].token == TokenType.Identity
    assert p.tokens[10].value == 'x'

    assert p.tokens[11].token == TokenType.Dot
    assert p.tokens[11].value == 'y'

    assert p.tokens[12].token == TokenType.LessThan
    assert p.tokens[12].value == ''
    
    assert p.tokens[13].token == TokenType.Identity
    assert p.tokens[13].value == '2'

    assert p.tokens[14].token == TokenType.BodyStart
    assert p.tokens[14].value == ''

    assert p.tokens[15].token == TokenType.Identity
    assert p.tokens[15].value == 'x'

    assert p.tokens[16].token == TokenType.Dot
    assert p.tokens[16].value == 'a'

    assert p.tokens[17].token == TokenType.Equal
    assert p.tokens[17].value == ''

    assert p.tokens[18].token == TokenType.Identity
    assert p.tokens[18].value == 'x'

    assert p.tokens[19].token == TokenType.Dot
    assert p.tokens[19].value == 'a'

    assert p.tokens[20].token == TokenType.Plus
    assert p.tokens[20].value == ''

    assert p.tokens[21].token == TokenType.Identity
    assert p.tokens[21].value == '1'

    assert p.tokens[22].token == TokenType.End
    assert p.tokens[22].value == ''

    assert p.tokens[23].token == TokenType.BodyEnd
    assert p.tokens[23].value == ''

    assert p.tokens[24].token == TokenType.Identity
    assert p.tokens[24].value == 'x'

    assert p.tokens[25].token == TokenType.Dot
    assert p.tokens[25].value == 'z'

    assert p.tokens[26].token == TokenType.Equal
    assert p.tokens[26].value == ''

    assert p.tokens[27].token == TokenType.Identity
    assert p.tokens[27].value == '5'

    assert p.tokens[28].token == TokenType.End
    assert p.tokens[28].value == ''
