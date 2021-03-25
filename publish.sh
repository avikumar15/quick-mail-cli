#!/bin/bash

python3 setup.py sdist bdist_wheel

echo "Build File Created!"

twine check dist/*

echo "Checks Passed"

twine upload dist/*

echo "Package Uploaded"
