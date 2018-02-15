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
fi

printf "\nSynchronizing with the latest changes on branch ${BRANCH}.\n"
git reset --hard origin/$BRANCH

if [ ! -z "$SCRIPT_INSTALL" ]; then
  printf "\n> $SCRIPT_INSTALL\n";
  $SCRIPT_INSTALL;
fi

if [ ! -z "$SCRIPT_BUILD" ]; then
  printf "\n> $SCRIPT_BUILD\n";
  $SCRIPT_BUILD;
fi

if [ ! -z "$SCRIPT_RELOAD" ]; then
  printf "\n> $SCRIPT_RELOAD\n";
  $SCRIPT_RELOAD;
fi

if [ ! -z "$SCRIPT_STATUS_CHECK\n" ]; then
  printf "\n> $SCRIPT_STATUS_CHECK";
  $SCRIPT_STATUS_CHECK;
fi
