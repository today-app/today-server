#!/bin/bash

BASEDIR=$(dirname $0)
cd $(dirname $BASEDIR)

# generate thrift files
for file in *.thrift; do
    echo "py:twisted $file"
    thrift --out gen -v --gen py:twisted $file
done
