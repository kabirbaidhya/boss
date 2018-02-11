#!/bin/sh

mkdir -p $REPOSITORY_PATH
cd $REPOSITORY_PATH

if [ -d ".git" ]; then
  printf "\nFetching the latest changes."
  git fetch --prune

  printf "\nChecking out to branch ${BRANCH}."
  git checkout -f $BRANCH
else
  git clone -b $BRANCH  $REPOSITORY_URL $REPOSITORY_PATH
fi;

printf "\nSynchronizing with the latest changes on branch ${BRANCH}.\n"
git reset --hard origin/$BRANCH
