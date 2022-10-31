#!/bin/bash
set -e

function get_pypy(){
  VERSION=$1
  rm -fr "${VERSION}-src.tar.bz2" "${VERSION}-osx64.tar.bz2" "${VERSION}-osx64" "${VERSION}-src"
  wget -S "https://downloads.python.org/pypy/${VERSION}-src.tar.bz2" && tar -xvf "${VERSION}-src.tar.bz2" > /dev/null
  wget -S "https://downloads.python.org/pypy/${VERSION}-osx64.tar.bz2" && tar -xvf "${VERSION}-osx64.tar.bz2" > /dev/null
}

function run_translate(){
  VERSION=$1
  FILENAME=$2
  "${PWD}/${VERSION}-osx64/bin/pypy" "${PWD}/${VERSION}-src/rpython/bin/rpython" "${PWD}/${FILENAME}"
}

# # 2.7
VERSION=pypy2.7-v7.3.9
get_pypy "${VERSION}"
run_translate "${VERSION}" "hello_world1.py"

# # 3.7
VERSION=pypy3.7-v7.3.9
get_pypy "${VERSION}"
run_translate "${VERSION}" "hello_world2.py"

# 3.9
VERSION=pypy3.9-v7.3.9
get_pypy "${VERSION}"
run_translate "${VERSION}" "hello_world2.py"
