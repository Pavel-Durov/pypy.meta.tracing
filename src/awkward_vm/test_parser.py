from src.awkward_vm.parser import clean_input, parse, TokenType


def test_new_object():
    p = parse("x = {};")
    
    assert len(p.tokens) == 4

    assert p.tokens[0].token.value == TokenType.Identity.value
    assert p.tokens[0].value == 'x'
    
    assert p.tokens[1].token.value == TokenType.Equal.value
    assert p.tokens[1].value == ''

    assert p.tokens[2].token.value == TokenType.NewObject.value
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

    assert p.tokens[2].token.value == TokenType.NewObject.value
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


def test_while_loop():
    p = parse( """
      while (x.y < 2) { 
        x.y = x.y + 1; 
      }
    """)

    assert p.tokens[0].token.value == TokenType.While.value
    assert p.tokens[0].value == ''
    
    assert p.tokens[1].token.value == TokenType.Identity.value
    assert p.tokens[1].value == 'x'

    assert p.tokens[2].token.value == TokenType.Dot.value
    assert p.tokens[2].value == 'y'

    assert p.tokens[3].token.value == TokenType.LessThan.value
    assert p.tokens[3].value == ''
    
    assert p.tokens[4].token.value == TokenType.Identity.value
    assert p.tokens[4].value == '2'

    assert p.tokens[5].token.value == TokenType.BodyStart.value
    assert p.tokens[5].value == ''

    assert p.tokens[6].token.value == TokenType.Identity.value
    assert p.tokens[6].value == 'x'

    assert p.tokens[7].token.value == TokenType.Dot.value
    assert p.tokens[7].value == 'y'

    assert p.tokens[8].token.value == TokenType.Equal.value
    assert p.tokens[8].value == ''

    assert p.tokens[9].token.value == TokenType.Identity.value
    assert p.tokens[9].value == 'x'

    assert p.tokens[10].token.value == TokenType.Dot.value
    assert p.tokens[10].value == 'y'

    assert p.tokens[11].token.value == TokenType.Plus.value
    assert p.tokens[11].value == ''

    assert p.tokens[12].token.value == TokenType.Identity.value
    assert p.tokens[12].value == '1'

    assert p.tokens[13].token.value == TokenType.End.value
    assert p.tokens[13].value == ''

    assert p.tokens[14].token.value == TokenType.BodyEnd.value
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

    assert p.tokens[0].token.value == TokenType.Identity.value
    assert p.tokens[0].value == 'x'
    
    assert p.tokens[1].token.value == TokenType.Equal.value
    assert p.tokens[1].value == ''

    assert p.tokens[2].token.value == TokenType.NewObject.value
    assert p.tokens[2].value == ''

    assert p.tokens[3].token.value == TokenType.End.value
    assert p.tokens[3].value == ''

    assert p.tokens[4].token.value == TokenType.Identity.value
    assert p.tokens[4].value == 'x'

    assert p.tokens[5].token.value == TokenType.Dot.value
    assert p.tokens[5].value == 'a'

    assert p.tokens[6].token.value == TokenType.Equal.value
    assert p.tokens[6].value == ''

    assert p.tokens[7].token.value == TokenType.Identity.value
    assert p.tokens[7].value == '1'

    assert p.tokens[8].token.value == TokenType.End.value
    assert p.tokens[8].value == ''

    assert p.tokens[9].token.value == TokenType.While.value
    assert p.tokens[9].value == ''
    
    assert p.tokens[10].token.value == TokenType.Identity.value
    assert p.tokens[10].value == 'x'

    assert p.tokens[11].token.value == TokenType.Dot.value
    assert p.tokens[11].value == 'y'

    assert p.tokens[12].token.value == TokenType.LessThan.value
    assert p.tokens[12].value == ''
    
    assert p.tokens[13].token.value == TokenType.Identity.value
    assert p.tokens[13].value == '2'

    assert p.tokens[14].token.value == TokenType.BodyStart.value
    assert p.tokens[14].value == ''

    assert p.tokens[15].token.value == TokenType.Identity.value
    assert p.tokens[15].value == 'x'

    assert p.tokens[16].token.value == TokenType.Dot.value
    assert p.tokens[16].value == 'a'

    assert p.tokens[17].token.value == TokenType.Equal.value
    assert p.tokens[17].value == ''

    assert p.tokens[18].token.value == TokenType.Identity.value
    assert p.tokens[18].value == 'x'

    assert p.tokens[19].token.value == TokenType.Dot.value
    assert p.tokens[19].value == 'a'

    assert p.tokens[20].token.value == TokenType.Plus.value
    assert p.tokens[20].value == ''

    assert p.tokens[21].token.value == TokenType.Identity.value
    assert p.tokens[21].value == '1'

    assert p.tokens[22].token.value == TokenType.End.value
    assert p.tokens[22].value == ''

    assert p.tokens[23].token.value == TokenType.BodyEnd.value
    assert p.tokens[23].value == ''

    assert p.tokens[24].token.value == TokenType.Identity.value
    assert p.tokens[24].value == 'x'

    assert p.tokens[25].token.value == TokenType.Dot.value
    assert p.tokens[25].value == 'z'

    assert p.tokens[26].token.value == TokenType.Equal.value
    assert p.tokens[26].value == ''

    assert p.tokens[27].token.value == TokenType.Identity.value
    assert p.tokens[27].value == '5'

    assert p.tokens[28].token.value == TokenType.End.value
    assert p.tokens[28].value == ''
