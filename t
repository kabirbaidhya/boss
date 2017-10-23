#!/bin/bash
# A simple script to automate tasks.

setup() {
  echo "Setting things up"
  pip install -r requirements-dev.txt
  python setup.py develop
  if ! [ -x "$(command -v chokidar)" ]; then
    npm install -g chokidar-cli
  fi
}

publish() {
  echo "Publishing"
  python setup.py egg_info
  python setup.py build
  python setup.py install
  python setup.py sdist upload -r pypi
}

test() {
  echo "Running tests"
  python -m "pytest"
}

testw() {
  # NOTE: This requires chokidar to be installed.
  # Install it with `npm install -g chokidar-cli if you haven't.
  # https://github.com/kimmobrunfeldt/chokidar-cli
  echo "Running tests (watch mode)"
  chokidar "**/*.py" --debounce=1000 --initial -c "python -m 'pytest'"
}

changelog() {
  # NOTE: This requires github_changelog_generator to be installed.
  # https://github.com/skywinder/github-changelog-generator

  if [ -z "$NEXT" ]; then
      NEXT="Next"
  fi

  echo "Generating changelog upto version: $NEXT"
  github_changelog_generator --pr-label "**Improvements:**" --issue-line-labels=ALL --future-release="$NEXT"
}

# Run command received from args.
$1
