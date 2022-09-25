
#!/bin/bash

set -e

VERSION=$1

if [ -z "$VERSION" ]; then
  echo "VERSION argument ismendatory!"
  exit 1
fi


IN_FILE_PATH=$2

if [ -z "$IN_FILE_PATH" ]; then
  echo "IN_FILE_PATH argument ismendatory!"
  exit 1
fi

JIT=$3

FILE_NAME=$(basename ${IN_FILE_PATH} | sed s/\.py$//)

OUT_FNAME=${PWD}/bin/${VERSION}/${VERSION}_$(git rev-parse HEAD)_${FILE_NAME}
TRANSLATED_C_FIE=${FILE_NAME}-c

if [ -z "${JIT}" ]; then
  echo "Translating without jit optimisations"
  python .pypy/rpython/translator/goal/translate.py ${IN_FILE_PATH}
  OUT_FNAME=${OUT_FNAME}-c
else
  echo "Translating with jit optimisations"
  python .pypy/rpython/translator/goal/translate.py --opt=jit ${IN_FILE_PATH}
  OUT_FNAME=${OUT_FNAME}-jit-c
fi

# copy to bin directory
mkdir -p ${PWD}/bin/${VERSION}

cp ${TRANSLATED_C_FIE} ${OUT_FNAME}
chmod u+x ${OUT_FNAME}

make git-lfs
