#!/bin/bash -l

PYTHON=$(which python3.6)
echo "PYTHON=${PYTHON}"

$PYTHON /check_changelog.py
