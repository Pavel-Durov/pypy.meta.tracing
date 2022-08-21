SHELL := /bin/bash
CWD := $(shell cd -P -- '$(shell dirname -- "$0")' && pwd -P)

init: 
	pyenv init
	pyenv shell 2.7.18 # not sure why but latest python version is not supported
	python --version
	python -m pip install virtualenv
	virtualenv --python=python2.7 venv
	source ./venv/bin/activate
	pip install -r requirements.txt
	hg clone https://foss.heptapod.net/pypy/pypy .pypy	

clear:
	rm tutorial-*-*