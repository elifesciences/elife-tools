#!/bin/bash
set -e

if [ ! -e venv/bin/"${python_versioned:-python}" ]; then
    rm -rf venv
fi
virtualenv --python="${python_versioned:-python}" venv
source venv/bin/activate
pip install -r requirements.txt
pip install coveralls
coverage run -m unittest discover elifetools/tests
COVERALLS_REPO_TOKEN=$(cat /etc/coveralls/tokens/elife-tools) coveralls
