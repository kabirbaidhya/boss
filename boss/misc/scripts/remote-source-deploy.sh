#!/bin/sh

# Initialize the deployment script
. "$INIT_SCRIPT_PATH"

mkdir -p $REPOSITORY_PATH
cd $REPOSITORY_PATH

if [ -d ".git" ]; then
  echo_info "Fetching the latest changes."
  git fetch --prune

  echo_info "Checking out to branch ${BRANCH}."
  git checkout -f $BRANCH
  echo;

  echo_info "Synchronizing with the latest changes on branch ${BRANCH}."
  git reset --hard origin/$BRANCH
else
  git clone -b $BRANCH  $REPOSITORY_URL $REPOSITORY_PATH
fi
echo;

if [ ! -z "$SCRIPT_INSTALL" ]; then
  echo_info "Running install"
  echo_fade "> $SCRIPT_INSTALL";
  $SCRIPT_INSTALL;
  echo;
fi

if [ ! -z "$SCRIPT_BUILD" ]; then
  echo_info "Running build"
  echo_fade "> $SCRIPT_BUILD";
  $SCRIPT_BUILD;
  echo;
fi

if [ ! -z "$SCRIPT_RELOAD" ]; then
  echo_info "Running reload"
  echo_fade "> $SCRIPT_RELOAD";
  $SCRIPT_RELOAD;
  echo;
fi

if [ ! -z "$SCRIPT_STATUS_CHECK\n" ]; then
  echo_info "Running status_check"
  echo_fade "> $SCRIPT_STATUS_CHECK";
  $SCRIPT_STATUS_CHECK;
  echo;
fi
