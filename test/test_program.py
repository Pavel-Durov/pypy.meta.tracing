from src.awk_vm.parser import parse
from src.awk_vm.program import AWKObject, eval, AWKHeap


def test_program_init_object():
    tokens = parse('x = {}; x.a = 123; x.b = 456789;')
    heap = eval(tokens, AWKHeap({}))
    assert len(heap.heap) == 1
    assert heap.get_obj('x').get_field('a') == 123
    assert heap.get_obj('x').get_field('b') == 456789

def test_program_object_attribute_assign():
    tokens = parse('x = {}; x.a = 0; x.b = 1; x.c = 2;')
    heap = eval(tokens, AWKHeap({}))
    assert len(heap.heap) == 1
    assert heap.get_obj('x').get_field('a') == 0
    assert heap.get_obj('x').get_field('b') == 1
    assert heap.get_obj('x').get_field('c') == 2

def test_program_reference_value():
    tokens = parse('x = {}; x.a = 1; y= {}; y.a = x.a;')
    heap = eval(tokens, AWKHeap({}))
    assert len(heap.heap) == 2
    assert heap.get_obj('x').get_field('a') == 1
    assert heap.get_obj('y').get_field('a') == 1
    

def test_program_expression():
    tokens = parse('x = {}; x.a = 1 + 1 + 2; x.b = 9 + 6;')
    heap = eval(tokens, AWKHeap({}))
    assert heap.get_obj('x').get_field('a') == 4
    assert heap.get_obj('x').get_field('b') == 15


def test_program_expression_reference():
    tokens = parse('''
      x = {}; 
      x.a = 1; 
      x.b = x.a + 1;
      z = {};
      z.a = x.a + x.b + 2;
      ''')
    heap = eval(tokens, AWKHeap({}))
    assert heap.get_obj('x').get_field('a') == 1
    assert heap.get_obj('x').get_field('b') == 2
    assert heap.get_obj('z').get_field('a') == 5


def test_program_while_loop_false_cond():
    tokens = parse('''
      x = {}; 
      x.a = 0; 
      while (x.a < 0) {
        x.a = x.a + 1;
      }
      ''')
    heap = eval(tokens, AWKHeap({}))
    assert heap.get_obj('x').get_field('a') == 0


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
    assert heap.get_obj('x').get_field('a') == 22
    assert heap.get_obj('x').get_field('b') == 8
    assert heap.get_obj('y').get_field('a') == 12

def test_program_existing_heap():
    p = AWKObject('p')
    p.set_field('a', 777)
    heap = { 'p': p }
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
    assert heap.get_obj('x').get_field('a') == 22
    assert heap.get_obj('x').get_field('b') == 8
    assert heap.get_obj('y').get_field('a') == 12
    assert heap.get_obj('p').get_field('a') == 777
