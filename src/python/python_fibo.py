import os
import sys


def fibonacci(n):
    num = 0
    n1 = 0
    n2 = 1
    count = 0
    while (count < n):
        num = n1 + n2
        n1 = n2
        n2 = num
        count += 1
    return num


def bubbles(elements):
  swapped = False

  for n in range(len(elements)-1, 0, -1):
    for i in range(n):
      if elements[i] > elements[i + 1]:
        swapped = True
        elements[i], elements[i + 1] = elements[i + 1], elements[i]
    if not swapped:
      print('@@', elements)
      return
  

def entry_point(argv):
    bubbles(range(0, 1000000))
    # index = int(argv[1])
    # num = fibonacci(index)
    # os.write(1, bytes('fobonucci %d number is %d\n' % (index, num), encoding='utf-8')) 
    return 0


def target(*args):
    """
    "target" returns the entry point.
    The translation process imports your module and looks for that name,
    calls it, and the function object returned is where it starts the translation.
    """
    return entry_point, None


if __name__ == '__main__':
    entry_point(sys.argv)
