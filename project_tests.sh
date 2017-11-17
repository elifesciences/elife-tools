#!/bin/bash
set -e

tox
. .toc/py35/bin/activate
pip install coveralls
COVERALLS_REPO_TOKEN=$(cat /etc/coveralls/tokens/elife-tools) coveralls
