from rpython.rlib.jit import JitDriver, purefunction, hint
from rpython.jit.codewriter.policy import JitPolicy


def jitpolicy(driver):
    return JitPolicy()


class C: pass


jitdriver = JitDriver(greens=["i"], reds=["c"])

def entry_point(argv):
  c = C()
  c.x = 0
  c.y = 1

  for i in range(100000):
    jitdriver.jit_merge_point(i=i, c=c)
    c.x += c.y
  
  return 0
  

def target(*args):
    """
    "target" returns the entry point.
    The translation process imports your module and looks for that name,
    calls it, and the function object returned is where it starts the translation.
    """
    return entry_point, None
 