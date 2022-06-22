#!/bin/bash
# Xiang Wang(ramwin@qq.com)

python3 setup.py sdist bdist_wheel
twine upload dist/*
