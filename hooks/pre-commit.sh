#!/usr/bin/bash

echo -e "Running pre-commit hooks.\n"
./hooks/lint.sh
./hooks/run-tests.sh

# Store exit value from command above and check if it's not zero.
if [ $? -ne 0 ]; then
 echo -e "\nFAILED: Tests must pass before commit!"
 exit 1
fi

