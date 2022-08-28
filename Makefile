SHELL := /bin/bash
CWD := $(shell cd -P -- '$(shell dirname -- "$0")' && pwd -P)

dev.setup.mac:
	brew update
	brew list hyperfine  || brew install hyperfine 
	brew list hg || brew install hgkubectl
	brew list pyenv || brew install pyenv
	
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
	rm ./*-c

setup:
	brew install hyperfine

# builds 
build-all: build-no-jit build-jit-not-optimised build-jit-purefunction build-jit-fixed-size-array build-jit-inlined-class

build-no-jit:
	PYTHONPATH=${PWD}/.pypy/ python ./.pypy/rpython/translator/goal/translate.py ${PWD}/src/no-jit.py

build-jit-%:
	PYTHONPATH=${PWD}/.pypy/ python ./.pypy/rpython/translator/goal/translate.py --opt=jit ${PWD}/src/jit-$*.py

# bench
bench:
	hyperfine './jit-fixed-size-array-c ./bf_programs/bench.bf'
	hyperfine './jit-inlined-class-c ./bf_programs/bench.bf'
	hyperfine './jit-not-optimised-c ./bf_programs/bench.bf'
	hyperfine './jit-purefunction-c ./bf_programs/bench.bf'
	hyperfine './no-jit-c ./bf_programs/bench.bf'
	