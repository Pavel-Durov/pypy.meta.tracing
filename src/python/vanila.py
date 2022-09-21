from rpython.rlib.jit import JitDriver, purefunction, hint
from rpython.jit.codewriter.policy import JitPolicy


def jitpolicy(driver):
    return JitPolicy()


class C: pass


jitdriver = JitDriver(greens=["i", "argv"], reds=["c"])

def entry_point(argv):
  c = C()
  c.x = 0
  c.y = 1
  i = 0
  while i < 1000000:
    jitdriver.jit_merge_point(i=i, c=c)
    c.x += c.y
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