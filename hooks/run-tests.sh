#!/usr/bin/env bash

# if any command returns error, exit and return the error
set -e

# always make sure we're at the root of our application.
cd "${0%/*}/.."

ADDED_FILES=$(git --no-pager diff --cached --name-only | cat)
TESTS=0

# Determine if tests should run.
for i in $ADDED_FILES
do
  if [ "${i: -3}" == ".py" ]
  then
    TESTS=1
  fi
done

# Run tests.
if [ "$TESTS" == 1 ]
then
  echo -e "\nRunning tests:\n"
  pipenv run pytest inquisitor/question.py --doctest-modules
else
  echo -e "\nNo tests to run.  Skipping.\n"
fi
