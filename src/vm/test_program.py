from src.vm.parser import parse


def test_program_init_object():
    p = parse("x = {};")
    p.evaluate()
    assert len(p.objects) == 1
    p.objects['x'] = {}


def test_program_object_attribute_assign():
    p = parse("x = {}; x.a = 0; x.b = 1; x.c = 2;")
    p.evaluate()
    assert len(p.objects) == 1
    p.objects['x'].props['a'] == 0
    p.objects['x'].props['b'] == 1

