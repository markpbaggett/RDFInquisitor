#!/usr/bin/bash

# get added files
ADDED_FILES=$(git --no-pager diff --cached --name-only | cat)
LINTING=0

# Run black on all python files and readd them.
for i in $ADDED_FILES
do
  if [ "${i: -3}" == ".py" ]
  then
    LINTING=1
    echo -e "\tBlackening $i."
    black "$i"
    git add "$i"
  fi
done

# If black is not run, say so.
if [ "$LINTING" == 0 ]
then
  echo -e "\tNo files blackened."
fi
