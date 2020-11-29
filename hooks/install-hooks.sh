#!/usr/bin/bash

GIT_DIR=$(git rev-parse --git-dir)
PATH_TO_OUTPUT=$(pwd)

echo "Installing hooks..."
# Symlink precommit in git repo to .git hooks
ln -s $PATH_TO_OUTPUT/hooks/pre-commit.sh $GIT_DIR/hooks/pre-commit
echo "Done!"

