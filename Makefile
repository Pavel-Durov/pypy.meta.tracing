SHELL := /bin/bash
CWD := $(shell cd -P -- '$(shell dirname -- "$0")' && pwd -P)

init: clone-pypy init-shell 

init-shell: 
	pyenv init
	pyenv shell 2.7.18 # not sure why but latest python version is not supported
	python -m pip install virtualenv
	virtualenv --python=python2.7 venv
	source ./venv/bin/activate
	pip install -r requirements.txt

clone-pypy:
	hg clone https://foss.heptapod.net/pypy/pypy .pypy	

clear:
	rm tutorial-*-*

jit-diff:
	git diff log/tutorial-2-jit-log-opt.logfile log/tutorial-2-jit-log-optimized-opt.logfile

setup:
	brew install hyperfine

non-optimized:
	PYTHONPATH=${PWD}/.pypy/ python ./.pypy/rpython/translator/goal/translate.py --opt=jit  ${PWD}/tutorial-2-not-optimised.py
	PYPYLOG=jit-log-opt:./log/tutorial-2-not-optimised-jit-log-opt.logfile ./tutorial-2-not-optimised-c ./example_programs/bench.bf
	hyperfine './tutorial-2-not-optimised-c ./example_programs/bench.bf'

optimised:
	PYTHONPATH=${PWD}/.pypy/ python ./.pypy/rpython/translator/goal/translate.py --opt=jit  ${PWD}/tutorial-2-optimised.py
	PYPYLOG=jit-log-opt:./log/tutorial-2-optimised-jit-log-opt.logfile ./tutorial-2-c ./example_programs/bench.bf
	hyperfine './tutorial-2-optimised-c ./example_programs/bench.bf'

inline:
	PYTHONPATH=${PWD}/.pypy/ python ./.pypy/rpython/translator/goal/translate.py --opt=jit ${PWD}/tutorial-2-inline.py
	PYPYLOG=jit-log-opt:./log/tutorial-2-inline-jit-log-opt.logfile ./tutorial-2-inline-c ./example_programs/bench.bf
	hyperfine './tutorial-2-inline-c ./example_programs/bench.bf'

fixed-size:
	PYTHONPATH=${PWD}/.pypy/ python ./.pypy/rpython/translator/goal/translate.py --opt=jit ${PWD}/tutorial-2-fixed-size.py
	PYPYLOG=jit-log-opt:./log/tutorial-2-fixed-size-jit-log-opt.logfile ./tutorial-2-fixed-size-c ./example_programs/bench.bf
	hyperfine './tutorial-2-fixed-size-c ./example_programs/bench.bf'