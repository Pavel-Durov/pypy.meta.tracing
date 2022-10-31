VERSION := 0.0.11
SHELL := /bin/bash
CWD := $(shell cd -P -- '$(shell dirname -- "$0")' && pwd -P)
VENV := venv
CONDA_ENV := meta-tracing
PYTHONPATH=${PWD}:${PWD}/.pypy/
PYPY_VERSION_ARTIFACT := pypy2.7-v7.3.9-src
.PHONY: test src

version:
	@echo $(VERSION)

dev.setup.mac:
	brew update
	brew list hyperfine  || brew install hyperfine 
	
dev.setup.linux:
	wget https://github.com/sharkdp/hyperfine/releases/download/v1.15.0/hyperfine_1.15.0_amd64.deb
	sudo dpkg -i hyperfine_1.15.0_amd64.deb

init: get-pypy init-env

init-env: 
	conda env create -f environment.yml
	conda init zsh && conda activate meta-tracing
	pip install -r requirements.txt

clean-pypy:
	rm -fr .pypy

get-pypy: clean-pypy
	wget -S  https://downloads.python.org/pypy/${PYPY_VERSION_ARTIFACT}.tar.bz2
	tar -xvf ${PYPY_VERSION_ARTIFACT}.tar.bz2
	mv ./${PYPY_VERSION_ARTIFACT} ./.pypy && rm "${PYPY_VERSION_ARTIFACT}.tar.bz2"

test-pypy:
	PYTHONPATH=${PYTHONPATH} python .pypy/rpython/translator/goal/translate.py ${PWD}/src/python/hello_world.py

git-lfs:
	git lfs track ./bin/**/*

test:
	pytest ./test

clear:
	conda init zsh
	conda deactivate
	conda remove -n meta-tracing --all
	rm ./*-c
		
conda-info:
	@echo CONDA_PREFIX=${CONDA_PREFIX}
	conda info --envs

# general
snapshot-id:
	@echo $(make version)_$(git rev-parse HEAD)_$(date +%s)

# AWK
run-awk:
	PYTHONPATH=${PYTHONPATH} python ./src/awk_vm/awk_vm.py ./programs/awk/loops.awk

translate-awk-vm:
	PYTHONPATH=${PYTHONPATH} python ./.pypy/rpython/translator/goal/translate.py --opt=jit ${PWD}/src/awk_vm/awk_vm.py

translate-awk-vm-no-jit:
	PYTHONPATH=${PYTHONPATH} python ./.pypy/rpython/translator/goal/translate.py ${PWD}/src/awk_vm/awk_vm.py

run-awk-c:
	PYPYLOG=jit-log-opt:./log/awk_vm_loops.logfile ./awk_vm-c ./programs/awk/loops.awk

# Python

pypy-translate-python-self-class:
	./scripts/translate_and_store.sh ${VERSION} ./src/python/python_self_like_class.py
	./scripts/translate_and_store.sh ${VERSION} ./src/python/python_self_like_class.py jit

pypy-translate-python-plain-class:
	./scripts/translate_and_store.sh ${VERSION} ./src/python/python_plain_class.py
	./scripts/translate_and_store.sh ${VERSION} ./src/python/python_plain_class.py jit
	
	

bench-python:
	hyperfine --warmup 10 './python_self_like_class-c' './python_plain_class-c' && hyperfine -m 20 -M 20 './python_self_like_class-c' './python_plain_class-c'


# BF
build-all: build-no-jit build-jit-not-optimised build-jit-purefunction build-jit-fixed-size-array build-jit-inlined-class

build-no-jit:
	PYTHONPATH=${PYTHONPATH} python ./.pypy/rpython/translator/goal/translate.py ${PWD}/src/bf/no-jit.py

build-jit-%:
	PYTHONPATH=${PYTHONPATH} python ./.pypy/rpython/translator/goal/translate.py --opt=jit ${PWD}/src/bf/jit-$*.py

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

bench-awk-vm:
	hyperfine --warmup 1 './awk_vm-c-0.0.9-get_opcode-purefunction-c ./programs/awk/loops.awk' './awk_vm-c-0.0.8-simple-heap-c ./programs/awk/loops.awk'
	hyperfine --export-json ${PWD}/log/hyperfine/hyperfine-$(git rev-parse HEAD)-$(date +%s).json -m 15 -M 15 './awk_vm-c-0.0.9-get_opcode-purefunction-c ./programs/awk/loops.awk' './awk_vm-c-0.0.8-simple-heap-c ./programs/awk/loops.awk'
	
# Docker
docker-build-ci: docker-login
	docker build -f docker/ci.Dockerfile -t meta-tracing:build-ci --platform=linux/amd64 .	
	docker tag meta-tracing:build-ci iamkimchi/pypy-trace:latest
	docker push iamkimchi/pypy-trace:latest

docker-build-%:	
	docker build -f docker/$*.Dockerfile -t meta-tracing:build-$* . #-platform=linux/amd64 .	

docker-entrypoint-override-%:
	docker run --entrypoint /bin/sh -t meta-tracing:build-$*

docker-run-%:
	docker run -t meta-tracing:build-$*

doccker-build-run-%: 
	make docker-build-$* 
	make docker-run-$*

docker-login:
	docker login --username iamkimchi