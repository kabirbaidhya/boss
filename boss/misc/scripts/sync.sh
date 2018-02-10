#!/bin/sh

mkdir -p $REPOSITORY_PATH
cd $REPOSITORY_PATH

if [ -d ".git" ]; then
  echo "Fetching the latest changes."
  git fetch --prune

  echo "Checking out to branch ${BRANCH}."
  git checkout -f $BRANCH
else
  git clone -b $BRANCH  $REPOSITORY_URL $REPOSITORY_PATH
fi;

echo "Synchronizing with the latest changes."
git reset --hard origin/$BRANCH
