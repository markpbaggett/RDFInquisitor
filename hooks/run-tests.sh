#!/usr/bin/env bash

set -e

cd "${0%/*}/.."

echo "Running tests"
pipenv run pytest inquisitor/question.py --doctest-modules

