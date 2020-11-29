#!/usr/bin/env bash

# if any command returns error, exit and return the error
set -e

# always make sure we're at the root of our application.
cd "${0%/*}/.."

echo "Running tests"
pipenv run pytest inquisitor/question.py --doctest-modules

