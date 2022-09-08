from src.awkward_vm.parser import parse
from src.awkward_vm.program import evaluate_program


def test_program_init_object():
    tokens = parse("x = {}; x.a = 123; x.b = 456789;")
    heap = {}
    evaluate_program(tokens, heap)
    assert len(heap) == 1
    assert heap['x']['a'] == 123
    assert heap['x']['b'] == 456789

def test_program_object_attribute_assign():
    tokens = parse("x = {}; x.a = 0; x.b = 1; x.c = 2;")
    heap = {}
    evaluate_program(tokens, heap)
    assert len(heap) == 1
    assert heap['x']['a'] == 0
    assert heap['x']['b'] == 1
    assert heap['x']['c'] == 2

def test_program_reference_value():
    tokens = parse("x = {}; x.a = 1; y= {}; y.a = x.a;")
    heap = {}
    evaluate_program(tokens, heap)
    assert len(heap) == 2
    assert heap['x']['a'] == 1
    assert heap['y']['a'] == 1
    

def test_program_expression():
    tokens = parse("x = {}; x.a = 1 + 1 + 2; x.b = 9 + 6;")
    heap = {}
    evaluate_program(tokens, heap)
    assert heap['x']['a'] == 4
    assert heap['x']['b'] == 15


def test_program_expression_reference():
    tokens = parse("""
      x = {}; 
      x.a = 1; 
      x.b = x.a + 1;
      z = {};
      z.a = x.a + x.b + 2;
      """)
    heap = {}
    evaluate_program(tokens, heap)
    assert heap['x']['a'] == 1
    assert heap['x']['b'] == 2
    assert heap['z']['a'] == 5


def test_program_while_loop_false_cond():
    tokens = parse("""
      x = {}; 
      x.a = 0; 
      while (x.a < 0) {
        x.a = x.a + 1;
      }
      """)
    heap = {}
    evaluate_program(tokens, heap)
    assert heap['x']['a'] == 0


def test_program_multi_while_loop():
    tokens = parse("""
      x = {}; 
      x.a = 10;
      x.b = 0 
      while (x.a < 20) {
        x.a = x.a + 3;
        x.b = x.b + 2
      }
      y={};
      y.a = 0; 
      while (y.a < 11) {
        y.a = y.a + 2;
      }
      """)
    heap = {}
    evaluate_program(tokens, heap)
    assert heap['x']['a'] == 22
    assert heap['x']['b'] == 8
    assert heap['y']['a'] == 12
