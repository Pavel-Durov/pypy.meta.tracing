from rpython.rlib.jit import JitDriver, purefunction, hint

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
    result = 'AWKObject(%s) fields\n' % self.name
    for key in self.fields:
      result += '  %s: %s' % (key, self.get_field(key))
    result += '\n'
    return result


class AWKSimpleObj(object):
  def __init__(self, name):
    self.name = name
    self.fields = {}

  def get_field(self, name):
    return self.fields[name]

  def set_field(self, name, value):
    self.fields[name] = value
  
  def __str__(self):
    result = 'AWKObject(%s) fields\n' % self.name
    for key in self.fields:
      result += '  %s: %s' % (key, self.get_field(key))
    result += '\n'
    return result


