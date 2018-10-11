#!/bin/bash
# A simple script to automate tasks.

setup() {
  echo "Setting things up"
  pip install -r requirements-dev.txt
  python setup.py develop
}

setup_ci() {
  echo "Setting things up for CI"
  pip install -r requirements-dev.txt
  pip install -U --editable .
}

publish_legacy() {
  test
  echo "Publishing (legacy way)"
  python setup.py egg_info
  python setup.py build
  python setup.py install
  python setup.py sdist upload -r pypi
}

publish() {
  test
  echo "Publishing"
  python setup.py clean
  python setup.py egg_info
  python setup.py build
  python setup.py install
  python setup.py sdist bdist_wheel
  twine upload dist/*
}

pep8() {
  echo "Running autopep8"
  autopep8 --in-place --aggressive --aggressive *.py
}

test() {
  echo "Running tests"
  python -m pytest -s
}

testw() {
  # NOTE: This requires chokidar to be installed.
  # Install it with `npm install -g chokidar-cli if you haven't.
  # https://github.com/kimmobrunfeldt/chokidar-cli
  echo "Running tests (watch mode)"
  chokidar "**/*.py" --debounce=1000 --initial -c "python -m pytest -s"
}

changelog() {
  # NOTE: This requires github_changelog_generator to be installed.
  # https://github.com/skywinder/github-changelog-generator

  if [ -z "$NEXT" ]; then
      NEXT="Next"
  fi

  echo "Generating changelog upto version: $NEXT"
  github_changelog_generator \
    --pr-label "**Improvements:**" \
    --issue-line-labels=ALL \
    --future-release="$NEXT" \
    --release-branch=master \
    --exclude-labels=unnecessary,duplicate,question,invalid,wontfix
}

# Run command received from args.
$1
