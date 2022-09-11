from src.awk_vm.parser import parse
from src.awk_vm.program import eval, AWKHeap


def test_program_init_object():
    tokens = parse('x = {}; x.a = 123; x.b = 456789;')
    heap = eval(tokens, AWKHeap({}))
    assert len(heap.objects) == 1
    assert heap.objects['x']['a'] == 123
    assert heap.objects['x']['b'] == 456789

def test_program_object_attribute_assign():
    tokens = parse('x = {}; x.a = 0; x.b = 1; x.c = 2;')
    heap = eval(tokens, AWKHeap({}))
    assert len(heap.objects) == 1
    assert heap.objects['x']['a'] == 0
    assert heap.objects['x']['b'] == 1
    assert heap.objects['x']['c'] == 2

def test_program_reference_value():
    tokens = parse('x = {}; x.a = 1; y= {}; y.a = x.a;')
    heap = eval(tokens, AWKHeap({}))
    assert len(heap.objects) == 2
    assert heap.objects['x']['a'] == 1
    assert heap.objects['y']['a'] == 1
    

def test_program_expression():
    tokens = parse('x = {}; x.a = 1 + 1 + 2; x.b = 9 + 6;')
    heap = eval(tokens, AWKHeap({}))
    assert heap.objects['x']['a'] == 4
    assert heap.objects['x']['b'] == 15


def test_program_expression_reference():
    tokens = parse('''
      x = {}; 
      x.a = 1; 
      x.b = x.a + 1;
      z = {};
      z.a = x.a + x.b + 2;
      ''')
    heap = eval(tokens, AWKHeap({}))
    assert heap.objects['x']['a'] == 1
    assert heap.objects['x']['b'] == 2
    assert heap.objects['z']['a'] == 5


def test_program_while_loop_false_cond():
    tokens = parse('''
      x = {}; 
      x.a = 0; 
      while (x.a < 0) {
        x.a = x.a + 1;
      }
      ''')
    heap = eval(tokens, AWKHeap({}))
    assert heap.objects['x']['a'] == 0


def test_program_multi_while_loop():
    tokens = parse('''
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
      ''')
    heap = eval(tokens, AWKHeap({}))
    assert heap.objects['x']['a'] == 22
    assert heap.objects['x']['b'] == 8
    assert heap.objects['y']['a'] == 12

def test_program_existing_heap():
    heap = { 'p': { 'a': 777 }}
    tokens = parse('''
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
      ''')
    heap = eval(tokens, AWKHeap(heap))
    assert heap.objects['x']['a'] == 22
    assert heap.objects['x']['b'] == 8
    assert heap.objects['y']['a'] == 12
    assert heap.objects['p']['a'] == 777
