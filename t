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

publish() {
  echo "Publishing"
  rm -rf dist build boss_cli.egg-info
  pip install -U .
  python setup.py sdist bdist_wheel
  twine upload --verbose dist/*
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
  echo "Running tests (watch mode)"
  ptw --runner "python -m pytest -s"
}

testw_chokidar() {
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

bump() {
  # Bump package version and generate changelog
  VERSION="${NEXT/v/}"

  # Update version in the following files
  sed -i "s/__version__ = .*/__version__ = '${VERSION}'/" boss/__init__.py
  sed -i "s/.*pip install boss-cli==.*/\$ pip install boss-cli==${VERSION}/" README.md
  
  # Generate change log
  changelog

  echo ""
  # Prepare to commit
  git add README.md boss/__init__.py CHANGELOG.md && \
    git commit -v --edit -m "Bump version $(git describe --abbrev=0 --tags) → ${VERSION}" && \
    git tag "$NEXT" && \
    echo -e "\nRelease tagged $NEXT"
  git push origin HEAD --tags
}

# Run command received from args.
$1
