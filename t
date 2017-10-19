#!/bin/bash
# A simple bash script to automate tasks.

publish() {
  echo 'Publishing'
  python setup.py egg_info
  python setup.py build
  python setup.py install
  python setup.py sdist upload -r pypi
}

test() {
  echo 'Running tests'
  python -m 'pytest'
}

testw() {
  echo 'Running tests (watch mode)'
  chokidar '**/*.py' --initial -c "python -m 'pytest'"
}

# Execute the command received from the args.
$1
