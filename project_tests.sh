#!/bin/bash
set -e

tox
. .tox/py3/bin/activate
pip install coveralls
COVERALLS_REPO_TOKEN=$(cat /etc/coveralls/tokens/elife-tools) coveralls
