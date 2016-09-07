#!/bin/bash
set -e

virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
pip install lettuce
pip install coveralls
cd elifetools/tests
lettuce
COVERALLS_REPO_TOKEN=$(cat /etc/coveralls/tokens/elife-tools) coveralls
