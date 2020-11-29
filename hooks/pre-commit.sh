#!/usr/bin/bash

echo "Running pre-commit hooks."
./hooks/run-tests.sh

if [ $? -ne 0 ]; then
 echo "Tests must pass before commit!"
 exit 1
fi

