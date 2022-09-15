from src.awk_vm.awk_object import AWKSelfLikeObj , AWKSimpleObj
from rpython.rlib.jit import purefunction

class AwkSelfLikeHeap():
  def __init__(self, heap):
    self.heap = heap

  def new_obj(self, name):
    self.heap[name] = AWKSelfLikeObj(name)
  
  @purefunction
  def get_obj(self, name):
    return self.heap.get(name)


class AwkSimpleHeap():
  def __init__(self, heap):
    self.heap = heap

  def new_obj(self, name):
    self.heap[name] = AWKSimpleObj(name)
  
  def get_obj(self, name):
    return self.heap.get(name)