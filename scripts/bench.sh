#!/bin/bash

VERSION=$1

if [ -z $VERSION]; then
  echo "Please provide project version to benchmark!"
  exit 1
fi

file_names=($( ls ./bin/${VERSION}/*-c ))
files_to_bench=$file_names
counter=0
for file_name in $file_names ; do
  
  files_to_bench="'./${files_to_bench}' './${file_name}'"
done

hyperfine --warmup 10 ${files_to_bench} && hyperfine -m 100 -M 100 ${files_to_bench}