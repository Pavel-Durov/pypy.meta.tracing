# bf.meta.tracing
Simple bf metatracing code following pypy tutorials

[Tutorial Part 1](https://morepypy.blogspot.com/2011/04/tutorial-writing-interpreter-with-pypy.html)

[Tutorial Part 2](https://morepypy.blogspot.com/2011/04/tutorial-part-2-adding-jit.html)

[Brainfuck](https://en.wikipedia.org/wiki/Brainfuck)

## Prerequisites
[pyenv](https://github.com/pyenv/pyenv) - support multi version python executable

## Getting Started

```shell
$ make init # virtual environment setup, pypy source code and shell config
```

### tutorial-1.py
```shell
$ PYTHONPATH=${PWD}/.pypy/ python ./.pypy/rpython/translator/goal/translate.py ${PWD}/tutorial-1.py
$ ./tutorial-1-c ./example_programs/*.b
```
### tutorial-2.py
```shell 
$ # TODO //
```
## Issues

### Python version
My local version (Python 3.8.13) wasn't supported when running pypy code, had to install Python 3.7.18.

### Broken links in tutorials

#### Tutorial: Writing an Interpreter with PyPy, Part 1 

https://bitbucket.org/brownan/pypy-tutorial/src/tip/example1.py

https://bitbucket.org/brownan/pypy-tutorial/src/tip/example2.py


### Broken imports in tutorials
```python
## No valid import, use os package instead
import sys

[translation:ERROR] AnnotatorError: 
Don't know how to represent <module 'sys' (built-in)>
    v8 = getattr((module sys), ('stdout'))
In <FunctionGraph of (pavel:11)mainloop at 0x105855848>:
Happened at file /Users/kimchi/git-repos/side-projects/simple.bf.meta.tracing/pavel.py line 34
```