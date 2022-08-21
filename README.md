# bf.meta.tracing
Simple bf metatracing code following pypy tutorials

## References

- [Tutorial Part 1](https://morepypy.blogspot.com/2011/04/tutorial-writing-interpreter-with-pypy.html)
- [Tutorial Part 2](https://morepypy.blogspot.com/2011/04/tutorial-part-2-adding-jit.html)
- [Brainfuck](https://en.wikipedia.org/wiki/Brainfuck)

## Tooling
Machine: Darwin MacBook-Pro-14-inch-2021-2.local 21.6.0 Darwin Kernel Version 21.6.0: Sat Jun 18 17:07:22 PDT 2022; root:xnu-8020.140.41~1/RELEASE_ARM64_T6000 arm64

[pyenv](https://github.com/pyenv/pyenv) - support multi version python executable

[hg](https://formulae.brew.sh/formula/mercurial#default) - Mercurial Distributed SCM

## Getting Started

```shell
$ make init # virtual environment setup, pypy source code and shell config
```

### tutorial-1.py
```shell
$ PYTHONPATH=${PWD}/.pypy/ python ./.pypy/rpython/translator/goal/translate.py ${PWD}/tutorial-1.py 2> ./log/tutorial-1-translate-opt.logfile
$ ./tutorial-1-c ./example_programs/*.b
```

### tutorial-2.py

```shell 
# non-optimized map
$ PYTHONPATH=${PWD}/.pypy/ python ./.pypy/rpython/translator/goal/translate.py --opt=jit  ${PWD}/tutorial-2.py 2> ./log/tutorial-2-translate-opt.logfile
$ PYPYLOG=jit-log-opt:./log/tutorial-2-jit-log-opt.logfile ./tutorial-2-c ./example_programs/*.b

# non-optimized map
$ PYTHONPATH=${PWD}/.pypy/ python ./.pypy/rpython/translator/goal/translate.py --opt=jit  ${PWD}/tutorial-2.py 2> tutorial-2-jit-log-opt-optimised.logfile
$ PYPYLOG=jit-log-opt:./log/tutorial-2-jit-log-optimized-opt.logfile ./tutorial-2-c ./example_programs/*.b

```
## Issues

### Python version
My local version (Python 3.8.13) wasn't supported when running pypy code, had to install Python 3.7.18.

### Broken links in tutorials

#### Tutorial: Writing an Interpreter with PyPy, Part 1 

https://bitbucket.org/brownan/pypy-tutorial/src/tip/example1.py

https://bitbucket.org/brownan/pypy-tutorial/src/tip/example2.py

#### Tutorial Part 2: Adding a JIT

https://bitbucket.org/brownan/pypy-tutorial/src/tip/example3.py

https://bitbucket.org/brownan/pypy-tutorial/src/tip/example4.py

https://bitbucket.org/brownan/pypy-tutorial/src/tip/example5.py

### Broken imports in tutorials
```python
## No valid import, use os package instead
import sys

[translation:ERROR] AnnotatorError: 
Don't know how to represent <module 'sys' (built-in)>
    v8 = getattr((module sys), ('stdout'))
In <FunctionGraph of (pavel:11)mainloop at 0x105855848>:
Happened at file /Users/kimchi/git-repos/side-projects/simple.bf.meta.tracing/pavel.py line 34

## Valid import: from rpython.rlib.jit import JitDriver
from pypy.rlib.jit import JitDriver 
## Valid import: from rpython.jit.codewriter.policy import JitPolicy
from pypy.jit.codewriter.policy import JitPolicy
```