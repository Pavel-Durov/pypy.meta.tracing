from src.awkward_vm.parser import parse


def test_program_init_object():
    p = parse("x = {};")
    p.evaluate()
    assert len(p.objects) == 1


def test_program_object_attribute_assign():
    p = parse("x = {}; x.a = 0; x.b = 1; x.c = 2;")
    p.evaluate()
    assert len(p.objects) == 1
    assert p.objects['x'].props['a'] == 0
    assert p.objects['x'].props['b'] == 1

def test_program_reference_value():
    p = parse("x = {}; x.a = 1; y= {}; y.a = x.a;")
    p.evaluate()
    assert len(p.objects) == 2
    assert p.objects['x'].props['a'] == 1
    assert p.objects['y'].props['a'] == 1
    

def test_program_expression():
    p = parse("x = {}; x.a = 1 + 1 + 2; x.b = 9 + 6;")
    p.evaluate()
    assert p.objects['x'].props['a'] == 4
    assert p.objects['x'].props['b'] == 15


def test_program_expression_reference():
    p = parse("""
      x = {}; 
      x.a = 1; 
      x.b = x.a + 1;
      z = {};
      z.a = x.a + x.b + 2;
      """)
    p.evaluate()
    assert p.objects['x'].props['a'] == 1
    assert p.objects['x'].props['b'] == 2
    assert p.objects['z'].props['a'] == 5



def test_program_while_loop_false_cond():
    p = parse("""
      x = {}; 
      x.a = 0; 
      while (x.a < 0) {
        x.a = x.a + 1;
      }
      """)
    p.evaluate()
    assert p.objects['x'].props['a'] == 0

def test_program_while_loop():
    p = parse("""
      x = {}; 
      x.a = 0;
      x.z = 0 
      while (x.a < 6) {
        x.a = x.a + 1;
        x.z = x.z + 2
      }
      x.b = 5; 
      """)
    p.evaluate()
    assert p.objects['x'].props['a'] == 6
    assert p.objects['x'].props['z'] == 2 * 6
    assert p.objects['x'].props['b'] == 5