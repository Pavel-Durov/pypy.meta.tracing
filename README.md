[![Test](https://github.com/Pavel-Durov/bf.meta.tracing/actions/workflows/test.yml/badge.svg)](https://github.com/Pavel-Durov/bf.meta.tracing/actions/workflows/test.yml)
[![RPython Translate](https://github.com/Pavel-Durov/bf.meta.tracing/actions/workflows/rpython.yml/badge.svg)](https://github.com/Pavel-Durov/bf.meta.tracing/actions/workflows/rpython.yml)

# bf.meta.tracing
Meta tracing exploration using PYPY.

## Getting Started

```shell
$ make dev.setup.mac # local environemnt setup
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

## Docker
This project uses docker containers for the sake of having consistent environment for running test and ci/cd jobs.

```shell
$ make docker-build-test # builds docker container
$ make docker-build-run-test # builds & runs test docker container
$ make docker-entrypoint-override-test # runs test docker with shell entrypoint
```

## Benchmarking
```shell
$ make bench # runs hyperfine benchmarking for all targets
```

## Tools

[conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) - Package, dependency and environment management for Python

[hg](https://formulae.brew.sh/formula/mercurial#default) - Mercurial Distributed SCM

[hyperfine](https://github.com/sharkdp/hyperfine) - A command-line benchmarking tool

[act](https://github.com/nektos/act) - Run your GitHub Actions locally

## Other Resources
[A gentle introduction to PyPy, Python performance and benchmarking](https://medium.com/@pav3ldurov/a-gentle-introduction-to-pypy-python-performance-and-benchmarking-3d0e5609985)

[Brainfuck](https://en.wikipedia.org/wiki/Brainfuck)

[BF Tests](https://github.com/ykjit/ykcbf/tree/master/lang_tests)

[Tutorial Issues](./docs/Issues.md)

[RPython](https://doc.pypy.org/en/latest/coding-guide.html#restricted-python)

[PypyTutorialKo](https://github.com/disjukr/pypy-tutorial-ko)

[Tutorial Part 1](https://morepypy.blogspot.com/2011/04/tutorial-writing-interpreter-with-pypy.html)

[Tutorial Part 2](https://morepypy.blogspot.com/2011/04/tutorial-part-2-adding-jit.html)

[Brainfuck](https://en.wikipedia.org/wiki/Brainfuck)
