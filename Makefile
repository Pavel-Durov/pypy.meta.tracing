SHELL := /bin/bash
CWD := $(shell cd -P -- '$(shell dirname -- "$0")' && pwd -P)
VENV := venv
CONDA_ENV := meta-tracing

PYTHONPATH=${PWD}:${PWD}/.pypy/

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

clear:
	conda init zsh
	conda deactivate
	conda remove -n meta-tracing --all
	rm ./*-c

setup:
	brew install hyperfine

run-awk:
	PYTHONPATH=$(PYTHONPATH) python ./src/awk_vm/awk_vm.py ./programs/awk/loops.awk

translate-awk-vm:
	PYTHONPATH=$(PYTHONPATH) python ./.pypy/rpython/translator/goal/translate.py --opt=jit ${PWD}/src/awkward_vm/main.py

translate-awk-vm-no-jit:
	PYTHONPATH=$(PYTHONPATH) python ./.pypy/rpython/translator/goal/translate.py ${PWD}/src/awkward_vm/main.py

run-awk-c:
	PYPYLOG=jit-log-opt:./log/awk_vm_loops.logfile ./main-c ./programs/awk/loops.awk


# builds 
build-all: build-no-jit build-jit-not-optimised build-jit-purefunction build-jit-fixed-size-array build-jit-inlined-class

build-no-jit:
	PYTHONPATH=$(PYTHONPATH) python ./.pypy/rpython/translator/goal/translate.py ${PWD}/src/no-jit.py

build-jit-%:
	PYTHONPATH=$(PYTHONPATH) python ./.pypy/rpython/translator/goal/translate.py --opt=jit ${PWD}/src/jit-$*.py

# bench
bench:
	hyperfine './jit-fixed-size-array-c ./program/bf/bench.bf'
	hyperfine './jit-inlined-class-c ./program/bf/bench.bf'
	hyperfine './jit-not-optimised-c ./program/bf/bench.bf'
	hyperfine './jit-purefunction-c ./program/bf/bench.bf'
	hyperfine './no-jit-c ./program/bf/bench.bf'
	
conda-info:
	echo CONDA_PREFIX=${CONDA_PREFIX}
	conda info --envs

test:
	pytest ./src