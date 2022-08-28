# bf.meta.tracing
Bf metatracing code following [pypy](https://www.pypy.org/) tutorials.

## Tutorials

- [Tutorial Part 1](https://morepypy.blogspot.com/2011/04/tutorial-writing-interpreter-with-pypy.html)
- [Tutorial Part 2](https://morepypy.blogspot.com/2011/04/tutorial-part-2-adding-jit.html)
- [Brainfuck](https://en.wikipedia.org/wiki/Brainfuck)

## Getting Started

```shell
$ dev.setup.mac # local environemnt setup
$ make init # virtual environment setup, pypy source code and shell config
```

## Build
```shell
$ make build-all # builds all src examples (might take a while)
```

## Jit logs
```shell
$ PYPYLOG=jit-log-opt:./log/${FILE_NAME}.logfile ${EXECUTABLE} ${BF_PROGRAM}
```

## Benchmarking
```shell
$ make bench # runs hyperfine benchmarking for all targets
```

![Hyperlane benchmark example](assets/bench_screenshot.png?raw=true "Title")


## Tools

[pyenv](https://github.com/pyenv/pyenv) - support multi version python executable

[hg](https://formulae.brew.sh/formula/mercurial#default) - Mercurial Distributed SCM

[hyperfine](https://github.com/sharkdp/hyperfine) - A command-line benchmarking tool


## Other Resources
[Brainfuck](https://en.wikipedia.org/wiki/Brainfuck)

[BF Tests](https://github.com/ykjit/ykcbf/tree/master/lang_tests)

[Tutorial Issues](./docs/Issues.md)

[RPython](https://doc.pypy.org/en/latest/coding-guide.html#our-runtime-interpreter-is-rpython)

[PypyTutorialKo](https://github.com/disjukr/pypy-tutorial-ko)