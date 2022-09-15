VERSION := 0.0.8
SHELL := /bin/bash
CWD := $(shell cd -P -- '$(shell dirname -- "$0")' && pwd -P)
VENV := venv
CONDA_ENV := meta-tracing
PYTHONPATH=${PWD}:${PWD}/.pypy/
.PHONY: test src

version:
	@echo $(VERSION)

dev.setup.mac:
	brew update
	brew list hyperfine  || brew install hyperfine 
	brew list hg || brew install hgkubectl
	brew list pyenv || brew install pyenv
	
init: clone-pypy init-env

init-env: 
	conda env create -f environment.yml
	conda init zsh && conda activate meta-tracing
	pip install -r requirements.txt

clone-pypy:
	hg clone https://foss.heptapod.net/pypy/pypy .pypy	

test:
	pytest ./test

clear:
	conda init zsh
	conda deactivate
	conda remove -n meta-tracing --all
	rm ./*-c
		
conda-info:
	echo CONDA_PREFIX=${CONDA_PREFIX}
	conda info --envs
	
# AWK
run-awk:
	PYTHONPATH=$(PYTHONPATH) python ./src/awk_vm/awk_vm.py ./programs/awk/loops.awk

translate-awk-vm:
	PYTHONPATH=$(PYTHONPATH) python ./.pypy/rpython/translator/goal/translate.py --opt=jit ${PWD}/src/awk_vm/awk_vm.py

translate-awk-vm-no-jit:
	PYTHONPATH=$(PYTHONPATH) python ./.pypy/rpython/translator/goal/translate.py ${PWD}/src/awk_vm/awk_vm.py

run-awk-c:
	PYPYLOG=jit-log-opt:./log/awk_vm_loops.logfile ./awk_vm-c ./programs/awk/loops.awk

# BF

build-all: build-no-jit build-jit-not-optimised build-jit-purefunction build-jit-fixed-size-array build-jit-inlined-class

build-no-jit:
	PYTHONPATH=$(PYTHONPATH) python ./.pypy/rpython/translator/goal/translate.py ${PWD}/src/bf/no-jit.py

build-jit-%:
	PYTHONPATH=$(PYTHONPATH) python ./.pypy/rpython/translator/goal/translate.py --opt=jit ${PWD}/src/bf/jit-$*.py

# BF Not Optimised
jit-not-optimised: build-jit-not-optimised
	PYPYLOG=jit-log-opt:./log/bf_not_optimised.logfile ./jit-not-optimised-c ./programs/bf/99bottles.b

# BF BENCH
bench:
	hyperfine './jit-fixed-size-array-c ./program/bf/bench.bf'
	hyperfine './jit-inlined-class-c ./program/bf/bench.bf'
	hyperfine './jit-not-optimised-c ./program/bf/bench.bf'
	hyperfine './jit-purefunction-c ./program/bf/bench.bf'
	hyperfine './no-jit-c ./program/bf/bench.bf'


