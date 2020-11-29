#!/usr/bin/bash

GIT_DIR=$(git rev-parse --git-dir)
PATH_TO_OUTPUT=$(pwd)

echo "Installing hooks..."
# this command creates symlink to our pre-commit script
ln -s $PATH_TO_OUTPUT/hooks/pre-commit.sh $GIT_DIR/hooks/pre-commit2
echo "Done!"

