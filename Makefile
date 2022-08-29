SHELL := /bin/bash
CWD := $(shell cd -P -- '$(shell dirname -- "$0")' && pwd -P)
VENV := venv
CONDA_ENV := bf-tracing
dev.setup.mac:
	brew update
	brew list hyperfine  || brew install hyperfine 
	brew list hg || brew install hgkubectl
	brew list pyenv || brew install pyenv
	
init: clone-pypy init-env

init-env: 
	conda env create -f environment.yml
	conda init zsh && conda activate $(CONDA_ENV)
	pip install -r requirements.txt

clone-pypy:
	hg clone https://foss.heptapod.net/pypy/pypy .pypy	

clear:
	conda init zsh
	conda deactivate
	conda remove -n $(CONDA_ENV) --all
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
	
conda-info:
	echo CONDA_PREFIX=${CONDA_PREFIX}
	conda info --envs