import os
import sys

def entry_point(argv):
    os.write(1, bytes("Hello World!\n"))
    return 0


def target(*args):
    return entry_point, None
