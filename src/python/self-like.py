from rpython.rlib.jit import JitDriver, purefunction, hint
from rpython.jit.codewriter.policy import JitPolicy

def jitpolicy(driver):
    return JitPolicy()

class SelfLikeMap(object):
    def __init__(self):
        self.attribute_indexes = {}
        self.other_maps = {}

    @purefunction
    def get_index(self, name):
        return self.attribute_indexes.get(name, -1)

    @purefunction
    def new_map_with_additional_attribute(self, name):
        if name not in self.other_maps:
            newmap = SelfLikeMap()
            newmap.attribute_indexes.update(self.attribute_indexes)
            newmap.attribute_indexes[name] = len(self.attribute_indexes)
            self.other_maps[name] = newmap
        return self.other_maps[name]

EMPTY_MAP = SelfLikeMap()

class AWKSelfLikeObj(object):
    def __init__(self, name):
        self.name = name
        self.map = EMPTY_MAP
        self.storage = []

    def get_field(self, name):
        map = hint(self.map, promote=True)
        index = map.get_index(name)
        if index != -1:
            return self.storage[index]
        raise AttributeError(name)

    def set_field(self, name, value):
        map = hint(self.map, promote=True)
        index = map.get_index(name)
        if index != -1:
            self.storage[index] = value
            return
        self.map = map.new_map_with_additional_attribute(name)
        self.storage.append(value)

    def __str__(self):
        result = "AWKObject(%s) fields\n" % self.name
        for key in self.fields.attribute_indexes:
            result += "  %s: %s" % (key, self.get_field(key))
        result += "\n"
        return result

jitdriver = JitDriver(greens=["i", "argv"], reds=["c"])


def entry_point(argv):
  i = 0
  c = AWKSelfLikeObj("test")
  # c.set_field("x", 0)
  # c.set_field("y", 1)

  while i < 1000000:
    jitdriver.jit_merge_point(i=i, argv=argv, c=c)
    c.set_field("x", 1)
    # x = c.get_field("x")
    # y = c.get_field("y")
    # c.set_field("x", x + y)
    
    i += 1
  return 0
  

def target(*args):
    """
    "target" returns the entry point.
    The translation process imports your module and looks for that name,
    calls it, and the function object returned is where it starts the translation.
    """
    return entry_point, None
 
if __name__ == '__main__':
    entry_point(None)