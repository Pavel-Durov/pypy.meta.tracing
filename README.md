[![Python Package using Conda](https://github.com/Pavel-Durov/bf.meta.tracing/actions/workflows/pytest.yml/badge.svg)](https://github.com/Pavel-Durov/bf.meta.tracing/actions/workflows/conda.yml)

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

## Awkward VM - (RPython VM)
Awkward VM implements simplistic virtual machine with object creation and simple integer operations.
Its call "Awkward" cause its what it is, clunky and awkward vm implementation.

[Awkward Program example](./programs/awkward/example.awk)


## Benchmarking
```shell
$ make bench # runs hyperfine benchmarking for all targets
```

![Hyperlane benchmark example](assets/bench_screenshot.png?raw=true "Title")


## Tools

[conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) - Package, dependency and environment management for Python

[hg](https://formulae.brew.sh/formula/mercurial#default) - Mercurial Distributed SCM

[hyperfine](https://github.com/sharkdp/hyperfine) - A command-line benchmarking tool

[act](https://github.com/nektos/act) - Run your GitHub Actions locally

## Other Resources
[Brainfuck](https://en.wikipedia.org/wiki/Brainfuck)

[BF Tests](https://github.com/ykjit/ykcbf/tree/master/lang_tests)

[Tutorial Issues](./docs/Issues.md)

[RPython](https://doc.pypy.org/en/latest/coding-guide.html#restricted-python)

[PypyTutorialKo](https://github.com/disjukr/pypy-tutorial-ko)