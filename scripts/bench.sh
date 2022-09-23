#!/bin/bash


file_names=($( ls ./bin/0.0.10/*-c ))
files_to_bench=$file_names
counter=0
for file_name in $file_names ; do
  
  files_to_bench="'./${files_to_bench}' './${file_name}'"
done

hyperfine --warmup 10 ${files_to_bench} && hyperfine -m 100 -M 100 ${files_to_bench}