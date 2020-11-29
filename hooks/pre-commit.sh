#!/usr/bin/bash

echo "Running pre-commit hooks."
./hooks/run-tests.sh

# Store exit value from command above and check if it's not zero.
if [ $? -ne 0 ]; then
 echo "Tests must pass before commit!"
 exit 1
fi

