#!/bin/sh

pipenv shell
m2r README.md
python setup.py sdist bdist_wheel
twine upload dist/*
