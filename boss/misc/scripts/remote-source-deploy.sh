#!/bin/sh

# Initialize the deployment script
. "$INIT_SCRIPT_PATH"

if [ ! -z "$SCRIPT_PRE_DEPLOY" ]; then
  echo_info "Running pre_deploy"
  echo_fade "> $SCRIPT_PRE_DEPLOY";
  $SCRIPT_PRE_DEPLOY;
  echo;
fi

mkdir -p $REPOSITORY_PATH
cd $REPOSITORY_PATH

if [ -d ".git" ]; then
  echo_info "Fetching the latest changes."
  git fetch --prune

  echo_info "Checking out to ${BRANCH}."
  git checkout -f $BRANCH
  echo;

  echo_info "Synchronizing with the latest changes of ${BRANCH}."

  # Check if the remote branch exists.
  cmd="$(git rev-parse --quiet --verify origin/$BRANCH)"
  ret_val=$?

  # If it does not exist assume it as a ref (commit / tag) and reset to it
  # If it exists, reset to the remote branch
  if [ $ret_val -ne 0 ]; then
    git reset --hard $BRANCH
  else
    git reset --hard origin/$BRANCH
  fi
else
  git clone -b $BRANCH  $REPOSITORY_URL $REPOSITORY_PATH
fi
echo;

if [ ! -z "$SCRIPT_PRE_INSTALL" ]; then
  echo_info "Running pre_install"
  echo_fade "> $SCRIPT_PRE_INSTALL";
  $SCRIPT_PRE_INSTALL;
  echo;
fi

if [ ! -z "$SCRIPT_INSTALL" ]; then
  echo_info "Running install"
  echo_fade "> $SCRIPT_INSTALL";
  $SCRIPT_INSTALL;
  echo;
fi

if [ ! -z "$SCRIPT_POST_INSTALL" ]; then
  echo_info "Running post_install"
  echo_fade "> $SCRIPT_POST_INSTALL";
  $SCRIPT_POST_INSTALL;
  echo;
fi

if [ ! -z "$SCRIPT_PRE_BUILD" ]; then
  echo_info "Running pre_build"
  echo_fade "> $SCRIPT_PRE_BUILD";
  $SCRIPT_PRE_BUILD;
  echo;
fi

if [ ! -z "$SCRIPT_BUILD" ]; then
  echo_info "Running build"
  echo_fade "> $SCRIPT_BUILD";
  $SCRIPT_BUILD;
  echo;
fi

if [ ! -z "$SCRIPT_POST_BUILD" ]; then
  echo_info "Running post_build"
  echo_fade "> $SCRIPT_POST_BUILD";
  $SCRIPT_POST_BUILD;
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

if [ ! -z "$SCRIPT_POST_DEPLOY" ]; then
  echo_info "Running post_deploy"
  echo_fade "> $SCRIPT_POST_DEPLOY";
  $SCRIPT_POST_DEPLOY;
  echo;
fi
