#!/bin/bash

set -e

VERSION=$1
MIN=$2
MAX=$3

if [ -z "$VERSION" ]; then
  echo "VERSION argument ismendatory!"
  exit 1
fi

if [ -z "$MIN" ]; then
  echo "MIN argument ismendatory!"
  exit 1
fi
if [ -z "$MIN" ]; then
  echo "MAX argument ismendatory!"
  exit 1
fi

file_names=($( ls ./bin/${VERSION}/*-c ))
files_to_bench=""
counter=0
for file_name in ./bin/${VERSION}/*-c ; do
  if [[ "$file_name" == *"-c"* ]]; then
    files_to_bench="${file_name} ${files_to_bench}"
  fi
done

hyperfine --warmup 10 ${files_to_bench}
hyperfine -m ${MIN} -M ${MAX} ${files_to_bench}