#!/bin/bash
python setup.py egg_info
python setup.py build
python setup.py install
python setup.py sdist upload -r pypi
