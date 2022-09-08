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
    assert tokens[2].value == ''

    assert tokens[3].token == TokenType.End
    assert tokens[3].value == ''



def test_new_object_with_attribute_set():
    tokens = parse("x = {}; x.y = 2;")
    assert len(tokens) == 9
    assert tokens[0].token == TokenType.Identity
    assert tokens[0].value == 'x'
    
    assert tokens[1].token == TokenType.Equal
    assert tokens[1].value == ''

    assert tokens[2].token == TokenType.NewObject
    assert tokens[2].value == ''

    assert tokens[3].token == TokenType.End
    assert tokens[3].value == ''

    assert tokens[4].token == TokenType.Identity
    assert tokens[4].value == 'x'

    assert tokens[5].token == TokenType.Dot
    assert tokens[5].value == 'y'

    assert tokens[6].token == TokenType.Equal
    assert tokens[6].value == ''

    assert tokens[7].token == TokenType.Identity
    assert tokens[7].value == '2'

    assert tokens[8].token == TokenType.End
    assert tokens[8].value == ''
    

def test_new_object_with_attribute_set_reference():
    tokens = parse("x.y = x.y + 9;")
    assert len(tokens) == 8
    assert tokens[0].token == TokenType.Identity
    assert tokens[0].value == 'x'
    
    assert tokens[1].token == TokenType.Dot
    assert tokens[1].value == 'y'

    assert tokens[2].token == TokenType.Equal
    assert tokens[2].value == ''

    assert tokens[3].token == TokenType.Identity
    assert tokens[3].value == 'x'

    assert tokens[4].token == TokenType.Dot
    assert tokens[4].value == 'y'

    assert tokens[5].token == TokenType.Plus
    assert tokens[5].value == ''

    assert tokens[6].token == TokenType.Identity
    assert tokens[6].value == '9'

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
    assert len(tokens) == 22


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
    
    assert tokens[1].token == TokenType.Identity
    assert tokens[1].value == 'x'

    assert tokens[2].token == TokenType.Dot
    assert tokens[2].value == 'y'

    assert tokens[3].token == TokenType.LessThan
    assert tokens[3].value == ''
    
    assert tokens[4].token == TokenType.Identity
    assert tokens[4].value == '2'

    assert tokens[5].token == TokenType.BodyStart
    assert tokens[5].value == ''

    assert tokens[6].token == TokenType.Identity
    assert tokens[6].value == 'x'

    assert tokens[7].token == TokenType.Dot
    assert tokens[7].value == 'y'

    assert tokens[8].token == TokenType.Equal
    assert tokens[8].value == ''

    assert tokens[9].token == TokenType.Identity
    assert tokens[9].value == 'x'

    assert tokens[10].token == TokenType.Dot
    assert tokens[10].value == 'y'

    assert tokens[11].token == TokenType.Plus
    assert tokens[11].value == ''

    assert tokens[12].token == TokenType.Identity
    assert tokens[12].value == '1'

    assert tokens[13].token == TokenType.End
    assert tokens[13].value == ''

    assert tokens[14].token == TokenType.BodyEnd
    assert tokens[14].value == ''
    


def test_while_loop():
    tokens = parse( """
      x = {};
      x.a = 1;
      while (x.y < 2) { 
       x.a = x.a + 1; 
      }
      x.z = 5;
    """)

    assert tokens[0].token == TokenType.Identity
    assert tokens[0].value == 'x'
    
    assert tokens[1].token == TokenType.Equal
    assert tokens[1].value == ''

    assert tokens[2].token == TokenType.NewObject
    assert tokens[2].value == ''

    assert tokens[3].token == TokenType.End
    assert tokens[3].value == ''

    assert tokens[4].token == TokenType.Identity
    assert tokens[4].value == 'x'

    assert tokens[5].token == TokenType.Dot
    assert tokens[5].value == 'a'

    assert tokens[6].token == TokenType.Equal
    assert tokens[6].value == ''

    assert tokens[7].token == TokenType.Identity
    assert tokens[7].value == '1'

    assert tokens[8].token == TokenType.End
    assert tokens[8].value == ''

    assert tokens[9].token == TokenType.While
    assert tokens[9].value == ''
    
    assert tokens[10].token == TokenType.Identity
    assert tokens[10].value == 'x'

    assert tokens[11].token == TokenType.Dot
    assert tokens[11].value == 'y'

    assert tokens[12].token == TokenType.LessThan
    assert tokens[12].value == ''
    
    assert tokens[13].token == TokenType.Identity
    assert tokens[13].value == '2'

    assert tokens[14].token == TokenType.BodyStart
    assert tokens[14].value == ''

    assert tokens[15].token == TokenType.Identity
    assert tokens[15].value == 'x'

    assert tokens[16].token == TokenType.Dot
    assert tokens[16].value == 'a'

    assert tokens[17].token == TokenType.Equal
    assert tokens[17].value == ''

    assert tokens[18].token == TokenType.Identity
    assert tokens[18].value == 'x'

    assert tokens[19].token == TokenType.Dot
    assert tokens[19].value == 'a'

    assert tokens[20].token == TokenType.Plus
    assert tokens[20].value == ''

    assert tokens[21].token == TokenType.Identity
    assert tokens[21].value == '1'

    assert tokens[22].token == TokenType.End
    assert tokens[22].value == ''

    assert tokens[23].token == TokenType.BodyEnd
    assert tokens[23].value == ''

    assert tokens[24].token == TokenType.Identity
    assert tokens[24].value == 'x'

    assert tokens[25].token == TokenType.Dot
    assert tokens[25].value == 'z'

    assert tokens[26].token == TokenType.Equal
    assert tokens[26].value == ''

    assert tokens[27].token == TokenType.Identity
    assert tokens[27].value == '5'

    assert tokens[28].token == TokenType.End
    assert tokens[28].value == ''
