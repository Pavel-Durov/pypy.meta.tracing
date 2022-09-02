from src.vm.parse import parse, TokenType


def test_new_object():
    tokens = parse(0, "x = {};")
    
    assert len(tokens) == 4

    assert tokens[0].token.value == TokenType.Identity.value
    assert tokens[0].value == 'x'
    
    assert tokens[1].token.value == TokenType.Equal.value
    assert tokens[1].value == ''

    assert tokens[2].token.value == TokenType.NewObjectStart.value
    assert tokens[2].value == ''

    assert tokens[3].token.value == TokenType.End.value
    assert tokens[3].value == ''



def test_new_object_with_attribute():
    tokens = parse(0, "x = {}; x.y = 2;")
    assert len(tokens) == 8
    assert tokens[0].token.value == TokenType.Identity.value
    assert tokens[0].value == 'x'
    
    assert tokens[1].token.value == TokenType.Equal.value
    assert tokens[1].value == ''

    assert tokens[2].token.value == TokenType.NewObjectStart.value
    assert tokens[2].value == ''

    assert tokens[3].token.value == TokenType.End.value
    assert tokens[3].value == ''

    assert tokens[4].token.value == TokenType.Dot.value
    assert tokens[4].value == 'y'

    assert tokens[5].token.value == TokenType.Equal.value
    assert tokens[5].value == ''

    assert tokens[6].token.value == TokenType.Identity.value
    assert tokens[6].value == '2'

    assert tokens[7].token.value == TokenType.End.value
    assert tokens[7].value == ''
    

    
    