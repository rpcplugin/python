#!/bin/bash

set -eu

SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do SOURCE="$(readlink "$SOURCE")"; done
DIR="$(cd -P "$(dirname "$SOURCE")" && pwd)"

cd "$DIR"

python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. countplugin1.proto
