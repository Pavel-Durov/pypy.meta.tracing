import os
import sys


def prime(n):
    primes = []
    for num in range(0, n):
        if num > 1:
            for i in range(2, num):
                if (num % i) == 0:
                    break
            else:
                primes.append(num)
    return primes


def write(s):
    os.write(1, bytes(s))


def entry_point(argv):
    num = int(argv[1])
    primes = prime(num)
    write('calculated primes: \n')
    for p in primes:
        write(str(p) + ' ')
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
